from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm, modelformset_factory
from django.forms.widgets import PasswordInput
from regimun_app.models import Conference, School, FacultySponsor, Committee, \
    Country

class NewSchoolForm(forms.Form):
    school_name = forms.CharField(label="Name", max_length=200)
    school_address_line_1 = forms.CharField(label="Mailing Address Line 1", max_length=200)
    school_address_line_2 = forms.CharField(label="Address, Line 2", max_length=200, required=False)
    school_city = forms.CharField(label="City", max_length=200)
    school_state = forms.CharField(label="State / Province / Region", max_length=200)
    school_zip = forms.CharField(label="ZIP / Postal Code", max_length=200, required=False)
    school_address_country = forms.CharField(label="Country", max_length=200, required=False)

class NewFacultySponsorForm(forms.Form):
    sponsor_username = forms.RegexField("\w+", label="Username", max_length=30, help_text="Alphanumeric characters only (letters, digits and underscores).")
    sponsor_password = forms.CharField(label="Password", max_length=128, widget=forms.PasswordInput)
    sponsor_first_name = forms.CharField(label="First name", max_length=30)
    sponsor_last_name = forms.CharField(label="Last name", max_length=30)
    sponsor_email = forms.EmailField(label="E-mail address", max_length=200)
    sponsor_phone = forms.CharField(label="Phone number", max_length=30)
    
class EditFacultySponsorForm(forms.Form):
    sponsor_first_name = forms.CharField(label="First name", max_length=30)
    sponsor_last_name = forms.CharField(label="Last name", max_length=30)
    sponsor_email = forms.EmailField(label="E-mail address", max_length=200)
    sponsor_phone = forms.CharField(label="Phone number", max_length=30)
    
class ConferenceForm(ModelForm):
    class Meta:
        model = Conference
        exclude = ('url_name',)

class BasicConferenceInfoForm(ModelForm):
    class Meta:
        model = Conference
        fields = ('date','location','logo','website_url',)

class OrganizationInfoForm(ModelForm):
    class Meta:
        model = Conference
        fields = ('organization_name','address_line_1','address_line_2','city','state','zip','address_country')

class SecretariatUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','password',)
        widgets = {
            'password' : PasswordInput,
        }

class SchoolMailingAddressForm(ModelForm):
    class Meta:
        model = School
        fields = ('address_line_1','address_line_2','city','state','zip','address_country')

CommitteeFormSet = modelformset_factory(Committee, can_delete=True, fields=('name',))

CountryFormSet = modelformset_factory(Country, can_delete=True, fields=('name','flag_icon',))
