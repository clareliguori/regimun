from django.db import models
from django.contrib.auth.models import User

class MailingAddress(models.Model):
	address_line_1 = models.CharField("Address Line 1", max_length=200)
	address_line_2 = models.CharField("Address, Line 2", max_length=200, blank=True)
	city = models.CharField(max_length=200)
	state = models.CharField("State / Province / Region", max_length=200)
	zip = models.CharField("ZIP / Postal Code", max_length=200,blank=True)
	country = models.CharField(max_length=200, blank=True)	

class Conference(models.Model):
	mailing_address = models.OneToOneField(MailingAddress)
	name = models.CharField(max_length=200, unique=True)
	date = models.DateField()
	location = models.CharField(max_length=200)
	logo = models.ImageField(upload_to="conference_logos")
	website_url = models.URLField(blank=True)
	organization_name = models.CharField("Organization/Company Name", max_length=200)
	
class Committee(models.Model):
	conference = models.ForeignKey(Conference)
	name = models.CharField(max_length=200)
	
class Country(models.Model):
	conference = models.ForeignKey(Conference)
	name = models.CharField(max_length=200)
	flag_icon = models.ImageField(upload_to="flag_icons")
	
class School(models.Model):
	mailing_address = models.OneToOneField(MailingAddress)
	name = models.CharField(max_length=200, unique=True)

class DelegatePosition(models.Model):
	country = models.ForeignKey(Country)
	committee = models.ForeignKey(Committee)
	school = models.ForeignKey(School)
	title = models.CharField(max_length=200, default="Delegate")
	
class Delegate(models.Model):
	position_assignment = models.OneToOneField(DelegatePosition)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	created = models.DateField(auto_now_add=True)
	last_modified = models.DateField(auto_now=True)

class FacultySponsor(models.Model):
	user = models.OneToOneField(User)
	school = models.ForeignKey(School)
	phone = models.CharField(max_length=30)
	