from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class Conference(models.Model):
	name = models.CharField(max_length=200, unique=True, help_text="This year's event name, such as CMUN 2010 or CMUN XXI")
	url_name = models.SlugField("Short Name", max_length=200, unique=True, help_text="You will use this name in your unique registration URL. Only alphanumeric characters, underscores, and hyphens are allowed. For example, CMUN2010.")
	date = models.DateField()
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
		Delegate.objects.filter(position_assignment__country__conference=self)
	
	class Meta:
		ordering = ('name',)
		
class FeeStructure(models.Model):
	conference = models.OneToOneField(Conference)
	per_school = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per_country = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per_sponsor = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per_delegate = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	late_registration_start_date = models.DateField()
	per_school_late_fee = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	per_delegate_late_fee = models.DecimalField(max_digits=11, decimal_places=2, default=0)

	def __unicode__(self):
		return self.conference.name

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

