from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.aggregates import Sum
from django.template.defaultfilters import date
from regimun_app.templatetags.currencyformat import currencyformat
import datetime

class Conference(models.Model):
	name = models.CharField(max_length=200, unique=True, help_text="This year's event name, such as CMUN 2010 or CMUN XXI")
	url_name = models.SlugField("Short Name", max_length=200, unique=True, help_text="You will use this name in your unique registration URL. Only alphanumeric characters, underscores, and hyphens are allowed. For example, CMUN2010.")
	start_date = models.DateField()
	end_date = models.DateField()
	location = models.CharField(max_length=200)
	logo = models.ImageField(upload_to="conference_logos", blank=True)
	email_address = models.EmailField()
	website_url = models.URLField("Website URL", blank=True)
	organization_name = models.CharField("Organization / Company / School", max_length=200, help_text="Who checks should be written to; Who issues invoices")
	address_line_1 = models.CharField("Street Address", max_length=200)
	address_line_2 = models.CharField("Address Line 2", max_length=200, blank=True)
	city = models.CharField(max_length=200)
	state = models.CharField("State / Province / Region", max_length=200)
	zip = models.CharField("ZIP / Postal Code", max_length=200,blank=True)
	address_country = models.CharField("Country", max_length=200, blank=True)
	def __unicode__(self):
		return self.name

	def delegates(self):
		return Delegate.objects.filter(position_assignment__country__conference=self)
	
	def delegates_count(self):
		return Delegate.objects.filter(position_assignment__country__conference=self).count()
	
	def delegate_count_preference_total(self):
		pref_sum = DelegateCountPreference.objects.filter(request__school__conference=self).aggregate(Sum('delegate_count'))
		if pref_sum['delegate_count__sum'] is None:
			return 0
		return pref_sum['delegate_count__sum']
	
	def delegate_count_preference_count(self):
		return DelegateCountPreference.objects.filter(request__school__conference=self).count()
	
	def country_preference_count(self):
		return CountryPreference.objects.filter(request__school__conference=self).values("request").distinct().count()
	
	def schools_assigned_countries_count(self):
		return DelegatePosition.objects.filter(school__conference=self).values("school").distinct().count()
	
	def assigned_countries_count(self):
		return DelegatePosition.objects.filter(school__conference=self).values("country").distinct().count()
	
	def assigned_positions_count(self):
		return DelegatePosition.objects.filter(school__conference=self).count()
	
	def chart_params(self, title):
		params = []
		params.append("chtt="+title)							# Chart title
		params.append("chs=600x200")							# Image size
		params.append("cht=bvg")								# Grouped bar chart								
		params.append("chbh=a,4,25")							# Bar width and spacing
		params.append("chf=bg,ls,90,EFEFEF,0.25,E0E0E0,0.25")	# Background color, linear stripes
		params.append("chxt=y,x")								# Axes
		params.append("chco=76A4FB")							# Bar color
		params.append("chma=|10,10")							# Margins
		params.append("chxs=0,676767,11.5,0,lt,676767|1,676767,11.5,0,lt,676767")	# Axis tick marks
		return params
	
	def by_month_graph(self, month_dict):
		params = []
		months_sorted = sorted(month_dict.keys())
		if len(months_sorted) > 0:
			first_month = months_sorted[0]
			last_month = months_sorted[-1]
			month_axis = "chxl=1:|"
			data_param = "chd=t:"
			data = []
			max_value = 0
			
			current_month = first_month
			while True:
				value = month_dict.get(current_month, 0)
				value_str = str(value)
				if isinstance(value, float):
					value_str = "$" + "%.2f" % value
				
				month_axis += current_month.strftime("%b %Y") + " (" + value_str + ")|"
				data.append(str(value))
				if value > max_value:
					max_value = value
				
				if current_month.month == last_month.month and current_month.year == last_month.year:
					break

				current_month = datetime.datetime(current_month.year + current_month.month/12, (current_month.month%12)+1, 1)
			
			params.append(month_axis)							# X axis labels
			params.append(data_param + ','.join(data))			# Data
			params.append("chds=0," + str(max_value))			# Data scaling
			params.append("chxr=0,0," + str(max_value))			# Y axis range
		return params

	def school_accounts_by_month_graph(self):
		
		# get the date each school joined
		school_dict = dict()
		for sponsor in FacultySponsor.objects.select_related('user','school').filter(school__conference=self):
			if sponsor.school in school_dict:
				if school_dict[sponsor.school] > sponsor.user.date_joined:
					school_dict[sponsor.school] = sponsor.user.date_joined
			else:
				school_dict[sponsor.school] = sponsor.user.date_joined
		
		# group the dates into months
		month_dict = dict()
		for school, date_joined in school_dict.items():
			month = datetime.datetime(date_joined.year, date_joined.month, 1)
			month_dict[month] = month_dict.get(month, 0) + 1
		
		url = "http://chart.apis.google.com/chart?"
		
		params = self.chart_params("School+Account+Creation+By+Month")
		params.extend(self.by_month_graph(month_dict))
		
		return url + '&'.join(params)
	
	def delegate_registration_by_month_graph(self):
		month_dict = dict()
		
		for delegate in Delegate.objects.filter(position_assignment__country__conference=self):
			month = datetime.datetime(delegate.last_modified.year, delegate.last_modified.month, 1)
			month_dict[month] = month_dict.get(month, 0) + 1
		
		url = "http://chart.apis.google.com/chart?"
		
		params = self.chart_params("Delegate+Registration+By+Month")
		params.extend(self.by_month_graph(month_dict))
		
		return url + '&'.join(params)
	
	def delegate_preference_by_month_graph(self):
		month_dict = dict()
		
		for delegate_count in DelegateCountPreference.objects.select_related().filter(request__school__conference=self):
			month = datetime.datetime(delegate_count.request.created.year, delegate_count.request.created.month, 1)
			month_dict[month] = month_dict.get(month, 0) + 1
		
		url = "http://chart.apis.google.com/chart?"
		
		params = self.chart_params("Delegation+Request+Submissions+By+Month")
		params.extend(self.by_month_graph(month_dict))
		
		return url + '&'.join(params)
	
	def payments_by_month_graph(self):
		month_dict = dict()
		
		for payment in Payment.objects.filter(school__conference=self):
			month = datetime.datetime(payment.date.year, payment.date.month, 1)
			month_dict[month] = month_dict.get(month, 0) + float(payment.amount)
		
		url = "http://chart.apis.google.com/chart?"
		
		params = self.chart_params("Fee+Payments+By+Month")
		params.extend(self.by_month_graph(month_dict))
		
		return url + '&'.join(params)
	
	class Meta:
		ordering = ('name',)
		
class FeeStructure(models.Model):
	conference = models.OneToOneField(Conference)
	per_school = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per_country = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per_sponsor = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per_delegate = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	late_registration_start_date = models.DateField("Late School Registration Start Date")
	late_delegate_registration_start_date = models.DateField("Late Delegate Registration Start Date")
	no_refunds_start_date = models.DateField()
	per_school_late_fee = models.DecimalField("Late School Registration Fee (Per School, Based on Country Preference Submissions)", max_digits=11, decimal_places=2, default=0)
	per_delegate_late_fee = models.DecimalField("Late Delegate Registration Fee (Per Delegate, Based on Delegate Name Submissions)", max_digits=11, decimal_places=2, default=0)

	def __unicode__(self):
		return self.conference.name
	
	def total_fee(self):
		valid_school_ids = []
		valid_schools = Delegate.objects.filter(position_assignment__school__conference=self.conference).values('position_assignment__school')
		for item in valid_schools:
			valid_school_ids.extend(item.values())
		valid_school_ids = set(valid_school_ids)
		
		total_school_fee = float(self.per_school * len(valid_school_ids))
		total_delegate_fee = float(self.per_delegate * DelegatePosition.objects.filter(school__id__in=valid_school_ids, delegate__isnull=False).count())
		total_late_delegate_fee = float(self.per_delegate_late_fee * DelegatePosition.objects.filter(school__id__in=valid_school_ids, delegate__isnull=False, delegate__last_modified__gte=self.late_delegate_registration_start_date).count())		
		total_country_fee = float(self.per_country * DelegatePosition.objects.filter(school__id__in=valid_school_ids, delegate__isnull=False).values('country','school').distinct().count())
		total_late_school_fee = float(self.per_school_late_fee * DelegationRequest.objects.filter(school__id__in=valid_school_ids, created__gte=self.late_registration_start_date).count())
		total_sponsor_fee = float(self.per_sponsor * FacultySponsor.objects.filter(school__id__in=valid_school_ids).count())
		
		total = total_school_fee + total_delegate_fee + total_late_delegate_fee + total_country_fee + total_late_school_fee + total_sponsor_fee
		
		return float(total)

	def total_payments(self):
		paysum = Payment.objects.filter(school__conference=self.conference).aggregate(Sum('amount'))
		if paysum['amount__sum'] is None:
			return 0.0
		return float(paysum['amount__sum'])
	
	def balance_due(self):
		return (self.total_fee() - self.total_payments())

class Committee(models.Model):
	conference = models.ForeignKey(Conference)
	name = models.CharField(max_length=200)
	url_name = models.SlugField("Short Name", max_length=200, help_text="You will use this name in unique registration URLs. Only alphanumeric characters, underscores, and hyphens are allowed.")
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('name',)
		
class Country(models.Model):
	conference = models.ForeignKey(Conference)
	name = models.CharField(max_length=200)
	url_name = models.SlugField("Short Name", max_length=200, help_text="You will use this name in unique registration URLs. Only alphanumeric characters, underscores, and hyphens are allowed.")
	country_code = models.CharField("ISO 3166-1 alpha-2 Country Code", max_length=2, blank=True, help_text='See the <a href="http://www.iso.org/iso/english_country_names_and_code_elements">official ISO 3166-1 alpha-2 code list</a>.')
	def __unicode__(self):
		return self.name

	def flag_icon(self):
		if self.country_code:
			return "icons/country_flags/flag-" + self.country_code.lower() + ".png"
		else:
			return ""
	
	class Meta:
		ordering = ('name',)	
	
class School(models.Model):
	conference = models.ForeignKey(Conference)
	name = models.CharField(max_length=200)
	url_name = models.SlugField("Short Name", max_length=200, help_text="You will use this name in unique registration URLs. Only alphanumeric characters, underscores, and hyphens are allowed.")
	address_line_1 = models.CharField("Address Line 1", max_length=200)
	address_line_2 = models.CharField("Address, Line 2", max_length=200, blank=True)
	city = models.CharField(max_length=200)
	state = models.CharField("State / Province / Region", max_length=200)
	zip = models.CharField("ZIP / Postal Code", max_length=200,blank=True)
	address_country = models.CharField("Country", max_length=200, blank=True)
	access_code = models.CharField(max_length=128)
	def __unicode__(self):
		return self.name
	
	def natural_key(self):
		return (self.name)
	
	class Meta:
		ordering = ('name',)	

	def get_html_mailing_address(self):
		ret = self.address_line_1;
		if len(self.address_line_2): ret += "<br/>" + self.address_line_2
		ret += "<br/>" + self.city + ", " + self.state
		if len(self.zip): ret += ", " + self.zip
		if len(self.address_country): ret += "<br/>" + self.address_country
		return ret;

	def get_delegate_positions(self):
		return self.delegateposition_set.all()

	def get_delegations(self):
		delegations = {}
		positions = DelegatePosition.objects.select_related('delegate','country','committee').filter(school=self).order_by('country__name','committee__name','delegate__last_name','delegate__first_name')
				
		for position in positions:
			delegations.setdefault(position.country,[])
			try:
				if position.delegate != None:
					delegations[position.country].append(position.delegate)
				else:
					delegations[position.country].append(position)
			except ObjectDoesNotExist:
				delegations[position.country].append(position)
		
		return sorted(delegations.items())
		
	def get_delegations_count(self):
		return self.delegateposition_set.filter(delegate__isnull=False).values('country').distinct().count()

	def get_delegate_request_count(self):
		count = 0
		try:
			count = int(self.delegationrequest.delegatecountpreference.delegate_count)
		except ObjectDoesNotExist:
			pass
		return count

	def get_delegate_request_date(self):
		try:
			return self.delegationrequest.created
		except ObjectDoesNotExist:
			return None
	
	def delegate_fee_from_request(self):
		return float(self.conference.feestructure.per_delegate * self.get_delegate_request_count())

	def get_filled_delegate_positions(self):
		return Delegate.objects.select_related('position_assignment__country').filter(position_assignment__school=self)

	def get_filled_delegate_positions_count(self):
		return Delegate.objects.filter(position_assignment__school=self).count()
	
	def get_late_delegate_registrations(self):
		return self.delegateposition_set.filter(delegate__isnull=False, delegate__last_modified__gte=self.conference.feestructure.late_delegate_registration_start_date)		

	def get_late_delegate_registrations_count(self, late_delegate_registration_start_date):
		return Delegate.objects.filter(position_assignment__school=self, last_modified__gte=late_delegate_registration_start_date).count()
	
	def country_fee(self):
		return float(self.conference.feestructure.per_country * self.get_delegations_count())
	
	def delegate_fee(self):
		return float(self.conference.feestructure.per_delegate * self.get_filled_delegate_positions_count())

	def sponsor_fee(self):
		return float(self.conference.feestructure.per_sponsor * self.facultysponsor_set.count())

	def delegate_late_fee(self):
		return float(self.conference.feestructure.per_delegate_late_fee * self.get_late_delegate_registrations_count(self.conference.feestructure.late_delegate_registration_start_date))

	def school_late_fee(self):
		try:
			request = DelegationRequest.objects.get(school=self)
			if request.created.date() >= self.conference.feestructure.late_registration_start_date:
				return float(self.conference.feestructure.per_school_late_fee)
		except ObjectDoesNotExist:
			pass
		return float(0.0)
	
	def total_fee(self):
		total = float(self.conference.feestructure.per_school) + self.country_fee() + self.delegate_fee() + self.sponsor_fee() + self.delegate_late_fee() + self.school_late_fee()
		return float(total)

	def total_fee_from_request(self):
		total = float(self.conference.feestructure.per_school) + self.delegate_fee_from_request() + self.sponsor_fee() + self.delegate_late_fee() + self.school_late_fee()
		return float(total)				
	
	def total_payments(self):
		sum = Payment.objects.filter(school=self).aggregate(Sum('amount'))
		if sum['amount__sum'] is None:
			return 0.0 
		return float(sum['amount__sum'])
	
	def balance_due(self):
		return (self.total_fee() - self.total_payments())

	def balance_due_from_request(self):
		return (self.total_fee_from_request() - self.total_payments())

class DelegatePosition(models.Model):
	country = models.ForeignKey(Country)
	committee = models.ForeignKey(Committee)
	school = models.ForeignKey(School, null=True)
	title = models.CharField(max_length=200, default="Delegate", help_text="Ambassador, Judge, etc")
	def __unicode__(self):
		return self.country.name + ", " + self.committee.name + ", " + self.school.name

	class Meta:
		ordering = ('school','country','committee','title')
	
class Delegate(models.Model):
	position_assignment = models.OneToOneField(DelegatePosition)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	created = models.DateField(auto_now_add=True)
	last_modified = models.DateField(auto_now=True)
	def get_full_name(self):
		return self.first_name + " " + self.last_name
	def __unicode__(self):
		return self.get_full_name()

	class Meta:
		ordering = ('last_name','first_name')	

class FacultySponsor(models.Model):
	user = models.OneToOneField(User, related_name="faculty_sponsor")
	school = models.ForeignKey(School)
	phone = models.CharField(max_length=30, blank=True)
	def __unicode__(self):
		return self.user.get_full_name()

	class Meta:
		ordering = ('user','phone',)

class Secretariat(models.Model):
	user = models.OneToOneField(User, related_name="secretariat_member")
	conference = models.ForeignKey(Conference)
	def __unicode__(self):
		return self.user.get_full_name()

	class Meta:
		ordering = ('user',)	

class DelegationRequest(models.Model):
	school = models.OneToOneField(School)
	created = models.DateTimeField(auto_now_add=True)

class CountryPreference(models.Model):
	request = models.ForeignKey(DelegationRequest)
	country = models.ForeignKey(Country)
	last_modified = models.DateTimeField()
	def __unicode__(self):
		return self.country.name + "/" + self.request.school.name
	
	class Meta:
		ordering = ('last_modified',)

class DelegateCountPreference(models.Model):
	request = models.OneToOneField(DelegationRequest)
	delegate_count = models.IntegerField()
	last_modified = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.request.school.name + "/" + str(self.delegate_count)
	
	class Meta:
		ordering = ('last_modified',)

PAYMENT_TYPES = (
    ('Cash', 'Cash'),
    ('Check', 'Check'),
    ('Credit Card', 'Credit Card'),
    ('Refund', 'Refund')
)

class Payment(models.Model):
	school = models.ForeignKey(School)
	type = models.CharField(max_length=12, choices=PAYMENT_TYPES)
	date = models.DateField()
	amount = models.DecimalField(max_digits=11, decimal_places=2, default=0, help_text="Enter negative value for refunds")
	notes = models.CharField(max_length=24, blank=True, help_text="Check number, credit card transaction ID, etc")

	def __unicode__(self):
		return self.school.name + "/" + str(self.amount)
	
