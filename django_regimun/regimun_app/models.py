from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.aggregates import Sum
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
	no_refunds_start_date = models.DateField()

	def __unicode__(self):
		return self.name

	def logo_width(self):
		if self.logo:
			return self.logo.width
		return 1
	
	def logo_height(self):
		if self.logo:
			return self.logo.height
		return 1

	def delegates(self):
		return Delegate.objects.filter(position_assignment__country__conference=self)
	
	def delegates_count(self):
		return Delegate.objects.filter(position_assignment__country__conference=self).count()
	
	def delegate_count_preference_total(self):
		pref_sum = DelegateCountPreference.objects.filter(request__conference=self).aggregate(Sum('delegate_count'))
		if pref_sum['delegate_count__sum'] is None:
			return 0
		return pref_sum['delegate_count__sum']
	
	def unassigned_delegate_position_count(self):
		return DelegatePosition.objects.filter(country__conference=self,school__isnull=True).count()
	
	def delegate_count_preference_count(self):
		return DelegateCountPreference.objects.filter(request__conference=self).count()
	
	def country_preference_count(self):
		return CountryPreference.objects.filter(request__conference=self).values("request").distinct().count()
	
	def schools_assigned_countries_count(self):
		return DelegatePosition.objects.filter(country__conference=self,school__isnull=False).values("school").distinct().count()
	
	def assigned_countries_count(self):
		return DelegatePosition.objects.filter(country__conference=self,school__isnull=False).values("country").distinct().count()
	
	def assigned_positions_count(self):
		return DelegatePosition.objects.filter(country__conference=self,school__isnull=False).count()
	
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
		for sponsor in FacultySponsor.objects.select_related('user','school').filter(conferences__id__exact=self.id):
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
		
		for delegate_count in DelegateCountPreference.objects.select_related().filter(request__conference=self):
			month = datetime.datetime(delegate_count.request.created.year, delegate_count.request.created.month, 1)
			month_dict[month] = month_dict.get(month, 0) + 1
		
		url = "http://chart.apis.google.com/chart?"
		
		params = self.chart_params("Delegation+Request+Submissions+By+Month")
		params.extend(self.by_month_graph(month_dict))
		
		return url + '&'.join(params)
	
	def delegate_preference_modified_by_month_graph(self):
		month_dict = dict()
		
		for delegate_count in DelegateCountPreference.objects.select_related().filter(request__conference=self):
			month = datetime.datetime(delegate_count.last_modified.year, delegate_count.last_modified.month, 1)
			month_dict[month] = month_dict.get(month, 0) + 1
		
		url = "http://chart.apis.google.com/chart?"
		
		params = self.chart_params("Delegation+Request+Last+Modified+By+Month")
		params.extend(self.by_month_graph(month_dict))
		
		return url + '&'.join(params)
	
	def payments_by_month_graph(self):
		month_dict = dict()
		
		for payment in Payment.objects.filter(conference=self):
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
	
	def __unicode__(self):
		return self.conference.name
	
	def total_fee(self):
		valid_school_ids = []
		valid_schools = Delegate.objects.filter(position_assignment__country__conference=self.conference).values('position_assignment__school')
		for item in valid_schools:
			valid_school_ids.extend(item.values())
		valid_school_ids = set(valid_school_ids)
		
		total = 0.0
		
		for fee in self.fee_set.all():
			count = 0
			if fee.per == 'Sch':
				count = len(valid_school_ids)
			elif fee.per == 'Del':
				count = Delegate.objects.filter(position_assignment__country__conference=self.conference).count()
			elif fee.per == 'Cou':
				count = DelegatePosition.objects.filter(country__conference=self.conference, delegate__isnull=False).values('country','school').distinct().count()
			elif fee.per == 'Spo':
				count = FacultySponsor.objects.filter(school__id__in=valid_school_ids,conferences__id__exact=self.conference.id).count()
			total += float(fee.amount * count)
		
		for penalty in self.datepenalty_set.all():
		
			# find the schools to charge
			valid_penalty_school_ids = []
			valid_schools = []
			if penalty.based_on == 'Co1':
				valid_schools = DelegationRequest.objects.filter(school__id__in=valid_school_ids, conference=self.conference, created__gte=penalty.start_date, created__lte=penalty.end_date).values('school')
			elif penalty.based_on == 'Co2':
				valid_schools = CountryPreference.objects.filter(school__id__in=valid_school_ids, request__conference=self.conference, last_modified__gte=penalty.start_date, last_modified__lte=penalty.end_date).values('request__school')
			elif penalty.based_on == 'DSu':
				valid_schools = Delegate.objects.filter(position_assignment__country__conference=self.conference, created__gte=penalty.start_date, created__lte=penalty.end_date).values('position_assignment__school')
			elif penalty.based_on == 'DMo':
				valid_schools = Delegate.objects.filter(position_assignment__country__conference=self.conference, last_modified__gte=penalty.start_date, last_modified__lte=penalty.end_date).values('position_assignment__school')
			
			# find the penalty count
			count = 0
			if len(valid_schools) > 0:
				for item in valid_schools:
					valid_penalty_school_ids.extend(item.values())
				valid_penalty_school_ids = set(valid_penalty_school_ids)
				
				if penalty.per == 'Sch':
					count = len(valid_penalty_school_ids)
				elif penalty.per == 'Del':
					count = DelegatePosition.objects.filter(school__id__in=valid_penalty_school_ids, country__conference=self.conference, delegate__isnull=False).count()
				elif penalty.per == 'DLa' and penalty.based_on == 'DSu':
					count = Delegate.objects.filter(position_assignment__school__id__in=valid_penalty_school_ids,position_assignment__country__conference=self.conference, created__gte=penalty.start_date, created__lte=penalty.end_date).count()
				elif penalty.per == 'DLa' and penalty.based_on == 'DMo':
					count = Delegate.objects.filter(position_assignment__school__id__in=valid_penalty_school_ids,position_assignment__country__conference=self.conference, last_modified__gte=penalty.start_date, last_modified__lte=penalty.end_date).count()
				elif penalty.per == 'Cou':
					count = DelegatePosition.objects.filter(school__id__in=valid_penalty_school_ids,country__conference=self.conference, delegate__isnull=False).values('country','school').distinct().count()
				elif penalty.per == 'Spo':
					count = FacultySponsor.objects.filter(school__id__in=valid_penalty_school_ids,conferences__id__exact=self.conference.id).count()
			total += float(penalty.amount * count)
			
		return float(total)

	def total_payments(self):
		paysum = Payment.objects.filter(conference=self.conference).aggregate(Sum('amount'))
		if paysum['amount__sum'] is None:
			return 0.0
		return float(paysum['amount__sum'])
	
	def balance_due(self):
		return (self.total_fee() - self.total_payments())

class Fee(models.Model):
	PER_CHOICES = (
        ('Sch', 'School'),
        ('Del', 'Delegate'),
        ('Cou', 'Country'),
        ('Spo', 'Sponsor'),
    )
	
	feestructure = models.ForeignKey(FeeStructure)
	name = models.CharField(max_length=200)
	amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per = models.CharField(max_length=3, choices=PER_CHOICES)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		ordering = ('name',)

class DatePenalty(models.Model):
	TYPE_CHOICES = (
        ('Co1', 'Country Preferences Created'),
        ('Co2', 'Country Preferences Modified'),
        ('DSu', 'Delegate Name Submitted'),
        ('DMo', 'Delegate Name Modified'),
    )
	
	PER_CHOICES = (
        ('Sch', 'School'),
        ('Del', 'All Delegates'),
        ('DLa', 'Delegates Within Date Range (use only with "Delegate Name"-based penalties)'),
        ('Cou', 'Country'),
        ('Spo', 'Sponsor'),
    )
	
	feestructure = models.ForeignKey(FeeStructure)
	name = models.CharField(max_length=200)
	amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per = models.CharField(max_length=3, choices=PER_CHOICES)
	based_on = models.CharField(max_length=3, choices=TYPE_CHOICES)
	start_date = models.DateField()
	end_date = models.DateField()
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		ordering = ('name',)

class Committee(models.Model):
	conference = models.ForeignKey(Conference)
	name = models.CharField(max_length=200)
	url_name = models.SlugField("Short Name", max_length=200, help_text="You will use this name in unique registration URLs. Only alphanumeric characters, underscores, and hyphens are allowed.")
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('name',)
		unique_together = (('name','conference'),('url_name','conference'))
		
class Country(models.Model):
	conference = models.ForeignKey(Conference)
	name = models.CharField(max_length=200)
	url_name = models.SlugField("Short Name", max_length=200, help_text="You will use this name in unique registration URLs. Only alphanumeric characters, underscores, and hyphens are allowed.")
	country_code = models.CharField("ISO 3166-1 alpha-2 Country Code", max_length=2, blank=True, help_text='See the <a href="http://www.iso.org/iso/country_codes/iso_3166_code_lists/country_names_and_code_elements.htm">official ISO 3166-1 alpha-2 code list</a>.')
	def __unicode__(self):
		return self.name

	def flag_icon(self):
		if self.country_code:
			return "icons/country_flags/flag-" + self.country_code.lower() + ".png"
		else:
			return ""
	
	class Meta:
		ordering = ('name',)	
		unique_together = (('name','conference'),('url_name','conference'))
	
class School(models.Model):
	conferences = models.ManyToManyField(Conference)
	name = models.CharField(max_length=200,unique=True)
	url_name = models.SlugField("Short Name", max_length=200, unique=True, help_text="You will use this name in unique registration URLs. Only alphanumeric characters, underscores, and hyphens are allowed.")
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

	def get_delegate_positions(self, conference):
		return DelegatePosition.objects.filter(school=self,country__conference=conference)

	def get_delegations(self, conference):
		delegations = {}
		positions = DelegatePosition.objects.select_related('delegate','country','committee').filter(school=self,country__conference=conference).order_by('country__name','committee__name','delegate__last_name','delegate__first_name')
				
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
		
	def get_delegations_count(self,conference):
		return DelegatePosition.objects.filter(school=self,country__conference=conference,delegate__isnull=False).values('country').distinct().count()
	
	def get_assigned_countries_count(self,conference):
		return DelegatePosition.objects.filter(school=self,country__conference=conference).values('country').distinct().count()
	
	def get_delegate_request_count(self,conference):
		count = 0
		try:
			count = DelegationRequest.objects.select_related().get(school=self,conference=conference).delegatecountpreference.delegate_count
		except ObjectDoesNotExist:
			pass
		return count

	def get_delegate_request_date(self,conference):
		try:
			return DelegationRequest.objects.get(school=self,conference=conference).created
		except ObjectDoesNotExist:
			return None
	
	def get_filled_delegate_positions(self,conference):
		return Delegate.objects.select_related('position_assignment__country').filter(position_assignment__school=self,position_assignment__country__conference=conference)

	def get_filled_delegate_positions_count(self,conference):
		return Delegate.objects.filter(position_assignment__school=self,position_assignment__country__conference=conference).count()
	
	def get_sponsors_count(self, conference):
		return FacultySponsor.objects.filter(school=self,conferences__id__exact=conference.id).count()
	
	def total_payments(self,conference):
		sum = Payment.objects.filter(school=self,conference=conference).aggregate(Sum('amount'))
		if sum['amount__sum'] is None:
			return 0.0 
		return float(sum['amount__sum'])
	
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
	conferences = models.ManyToManyField(Conference)
	def __unicode__(self):
		return self.user.get_full_name()

	class Meta:
		ordering = ('user','phone',)

class Secretariat(models.Model):
	user = models.OneToOneField(User, related_name="secretariat_member")
	conferences = models.ManyToManyField(Conference)
	def __unicode__(self):
		return self.user.get_full_name()

	class Meta:
		ordering = ('user',)	

class DelegationRequest(models.Model):
	school = models.ForeignKey(School)
	conference = models.ForeignKey(Conference)
	created = models.DateTimeField(auto_now_add=True)
	unique_together = ('school','conference')

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
	conference = models.ForeignKey(Conference)
	type = models.CharField(max_length=12, choices=PAYMENT_TYPES)
	date = models.DateField()
	amount = models.DecimalField(max_digits=11, decimal_places=2, default=0, help_text="Enter negative value for refunds")
	notes = models.CharField(max_length=24, blank=True, help_text="Check number, credit card transaction ID, etc")

	def __unicode__(self):
		return self.school.name + "/" + str(self.amount)
	
