from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
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
	
	def delegate_count_preference_total(self):
		total = 0
		prefs = DelegateCountPreference.objects.filter(school__conference=self)
		for pref in prefs:
			total += pref.delegate_count
		
		return total
	
	def delegate_count_preference_count(self):
		return DelegateCountPreference.objects.filter(school__conference=self).count()
	
	def country_preference_count(self):
		return CountryPreference.objects.filter(school__conference=self).values("school").distinct().count()
	
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
				
				current_month = datetime.datetime(current_month.year+(current_month.month+1)/12, (current_month.month+1)%12, 1)	
			
			params.append(month_axis)							# X axis labels
			params.append(data_param + ','.join(data))			# Data
			params.append("chds=0," + str(max_value))			# Data scaling
			params.append("chxr=0,0," + str(max_value))			# Y axis range
		return params

	def school_accounts_by_month_graph(self):
		month_dict = dict()
		
		for school in self.school_set.all():
			sponsors = FacultySponsor.objects.filter(school=school).order_by('user__date_joined')
			if len(sponsors) > 0:
				month = datetime.datetime(sponsors[0].user.date_joined.year, sponsors[0].user.date_joined.month, 1)
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
		
		for delegate_count in DelegateCountPreference.objects.filter(school__conference=self):
			month = datetime.datetime(delegate_count.last_modified.year, delegate_count.last_modified.month, 1)
			month_dict[month] = month_dict.get(month, 0) + 1
		
		url = "http://chart.apis.google.com/chart?"
		
		params = self.chart_params("Delegate+Count+Request+Submissions+By+Month")
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
	late_registration_start_date = models.DateField()
	no_refunds_start_date = models.DateField()
	per_school_late_fee = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per_delegate_late_fee = models.DecimalField(max_digits=11, decimal_places=2, default=0)

	def __unicode__(self):
		return self.conference.name
	
	def total_fee(self):
		total = 0.0
		for school in School.objects.select_related().filter(conference=self.conference):
			if len(school.get_filled_delegate_positions()) > 0:
				total += school.total_fee()
		return float(total)
	
	def total_payments(self):
		total = 0.0
		for payment in Payment.objects.filter(school__conference=self.conference):
			total += float(payment.amount)
		
		return float(total)
	
	def balance_due(self):
		balance = 0.0
		for school in School.objects.select_related().filter(conference=self.conference):
			if len(school.get_filled_delegate_positions()) > 0:
				balance += school.balance_due()
		return float(balance)

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
		return DelegatePosition.objects.filter(school=self)

	def get_delegations(self):
		delegations = {}
		positions = self.get_delegate_positions()
		current_country = Country()
		
		for position in positions:
			if position.country.pk != current_country.pk:
				current_country = position.country
				delegations[current_country] = []
			try:
				delegations[current_country].append(position.delegate)
			except ObjectDoesNotExist:
				delegations[current_country].append(position)
		return delegations

	def get_filled_delegate_positions(self):
		return DelegatePosition.objects.filter(school=self, delegate__isnull=False)

	def get_late_delegate_registrations(self):
		return DelegatePosition.objects.filter(school=self, delegate__isnull=False, delegate__last_modified__gte=self.conference.feestructure.late_registration_start_date)		

	def country_fee(self):
		return (self.conference.feestructure.per_country * len(self.get_delegations().keys()))
	
	def delegate_fee(self):
		return (self.conference.feestructure.per_delegate * len(self.get_filled_delegate_positions()))

	def sponsor_fee(self):
		return (self.conference.feestructure.per_sponsor * self.facultysponsor_set.count())

	def delegate_late_fee(self):
		return (self.conference.feestructure.per_delegate_late_fee * len(self.get_late_delegate_registrations()))
	
	def total_fee(self):
		total = self.conference.feestructure.per_school + self.country_fee() + self.delegate_fee() + self.sponsor_fee() + self.delegate_late_fee()
		if len(self.get_late_delegate_registrations()) > 0:
			total += self.conference.feestructure.per_school_late_fee
		return float(total)
	
	def total_payments(self):
		total = 0.0
		
		payments = Payment.objects.filter(school=self)
		for payment in payments:
			total += float(payment.amount)
		
		return float(total)
	
	def balance_due(self):
		return (self.total_fee() - self.total_payments())

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
	
class CountryPreference(models.Model):
	country = models.ForeignKey(Country)
	school = models.ForeignKey(School)
	last_modified = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.country + "/" + self.school
	
	class Meta:
		ordering = ('last_modified',)

class DelegateCountPreference(models.Model):
	school = models.ForeignKey(School)
	delegate_count = models.IntegerField()
	last_modified = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.school + "/" + self.delegate_count
	
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
		return self.school + "/" + self.amount
	