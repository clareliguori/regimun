from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm, modelformset_factory
from django.forms.widgets import PasswordInput, HiddenInput, TextInput
from regimun_app.models import Conference, School, Committee, Country, \
    FeeStructure, Delegate

class jEditableForm(forms.Form):
    id = forms.CharField(max_length=200)
    value = forms.CharField(max_length=200)

class UploadFileForm(forms.Form):
    file = forms.FileField()

class DetailedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",'first_name','last_name', 'email')

class NewSchoolForm(forms.Form):
    school_name = forms.CharField(label="Name", max_length=200)
    school_address_line_1 = forms.CharField(label="Mailing Address Line 1", max_length=200)
    school_address_line_2 = forms.CharField(label="Address, Line 2", max_length=200, required=False)
    school_city = forms.CharField(label="City", max_length=200)
    school_state = forms.CharField(label="State / Province / Region", max_length=200)
    school_zip = forms.CharField(label="ZIP / Postal Code", max_length=200, required=False)
    school_address_country = forms.CharField(label="Country", max_length=200, required=False)

class SchoolNameForm(ModelForm):
    class Meta:
        model = School
        fields = ('name',)

class NewFacultySponsorForm(forms.Form):
    sponsor_username = forms.RegexField("\w+", label="Username", max_length=30, help_text="Alphanumeric characters only (letters, digits and underscores).")
    sponsor_password = forms.CharField(label="Password", max_length=128, widget=forms.PasswordInput)
    sponsor_first_name = forms.CharField(label="First name", max_length=30)
    sponsor_last_name = forms.CharField(label="Last name", max_length=30)
    sponsor_email = forms.EmailField(label="E-mail address", max_length=200)
    sponsor_phone = forms.CharField(label="Phone number", max_length=30)
    
class EditFacultySponsorForm(forms.Form):
    sponsor_pk = forms.DecimalField(widget=HiddenInput())
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
        fields = ('date','location','website_url','logo')

class FeeStructureForm(ModelForm):
    class Meta:
        model = FeeStructure
        exclude = ('conference')
        widgets = {
            'per_school': TextInput(attrs={'class': "auto {aSign: '$'}"}),
            'per_country': TextInput(attrs={'class': "auto {aSign: '$'}"}),
            'per_sponsor': TextInput(attrs={'class': "auto {aSign: '$'}"}),
            'per_delegate': TextInput(attrs={'class': "auto {aSign: '$'}"}),
            'per_school_late_fee': TextInput(attrs={'class': "auto {aSign: '$'}"}),
            'per_delegate_late_fee': TextInput(attrs={'class': "auto {aSign: '$'}"}),            
        }

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

class NewCommitteeForm(ModelForm):
    class Meta:
        model = Committee
        fields=('name',)

    def clean_name(self):
        data = self.cleaned_data['name']
        if Committee.objects.filter(name=data).count() > 0:
            raise forms.ValidationError("A committee already exists with this name.")

        return data

class NewCountryForm(ModelForm):
    class Meta:
        model = Country
        fields=('name','flag_icon',)

    def clean_name(self):
        data = self.cleaned_data['name']
        if Country.objects.filter(name=data).count() > 0:
            raise forms.ValidationError("A country already exists with this name.")

        return data

class DelegateNameForm(ModelForm):
    class Meta:
        model = Delegate
        fields=('first_name','last_name')

CommitteeFormSet = modelformset_factory(Committee, can_delete=True, fields=('name',))

CountryFormSet = modelformset_factory(Country, can_delete=True, fields=('name','flag_icon',))
