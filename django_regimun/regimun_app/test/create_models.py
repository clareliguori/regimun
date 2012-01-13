from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from regimun_app.models import Conference, Committee, Country, School
from regimun_app.test.login import LoginTestCase
from regimun_app.test.test_data import *
from regimun_app.test.utils import file_len
from settings import MEDIA_ROOT
import datetime
import json
import settings

class CreateConferenceTest(LoginTestCase):
    def test_create_conference(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password))
        
        response = self.client.get('/new-conference/', follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        if self.is_logged_in():
            self.assertTemplateUsed(response, 'conference/create-conference.html')
            if self.is_staff_client():
                self.assertContains(response, "Conference Information")
            else:
                self.assertContains(response, "You do not have access to this page")
        else:
            self.assertRedirects(response, settings.LOGIN_URL + '?next=/new-conference/')
        
        conference_date_1 = datetime.date.today() + datetime.timedelta(6*365/12)
        conference_date_2 = conference_date_1 + datetime.timedelta(4)

        for conference_name in conferences:
            secretariat_user = secretariat_by_conference[conference_name]
            conf_dict = {'name': conference_name,
                           'start_date': conference_date_1.strftime("%m/%d/%Y"),
                           'end_date': conference_date_2.strftime("%m/%d/%Y"),
                           'location':  conference_name + " Location",
                           'email_address' : secretariat_user['username'] + '@test.com',
                           'website_url' : 'http://www.google.com',
                           'organization_name' : conference_name + ", Inc",
                           'address_line_1' : '1 ' + conference_name  + " Lane",
                           'address_line_2' : "Mailbox A",
                           'city' : 'Austin',
                           'state' : 'TX',
                           'zip' : '77777',
                           'address_country' : 'USA'}
            
            # empty secretariat name
            response = self.client.post('/new-conference/', conf_dict, follow=True)
            self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
            if self.is_logged_in():
                self.assertTemplateUsed(response, 'conference/create-conference.html')
                if self.is_staff_client():
                    self.assertContains(response, "Conference Information")
                    self.assertFormError(response, 'secretariat_form', 'username', "This field is required.")
                else:
                    self.assertContains(response, "You do not have access to this page")
            else:
                self.assertRedirects(response, settings.LOGIN_URL + '?next=/new-conference/')
            
            conf_dict['username'] = secretariat_user['username']
            conf_dict['password1'] = secretariat_user['password']
            conf_dict['password2'] = secretariat_user['password']
            
            response = self.client.post('/new-conference/', conf_dict, follow=True)
            self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
            if self.is_logged_in():
                if self.is_staff_client():
                    self.assertRedirects(response, '/' + slugify(conference_name) + '/secretariat/')
                    self.assertTemplateUsed(response, 'secretariat/index.html')
                    
                    # test that the secretariat user was created and conference object was created
                    secretariat_user = User.objects.get(username=secretariat_user['username'])
                    conference = Conference.objects.get(name=conference_name)
                    
                    secretariat_user.secretariat_member.conferences.get(id=conference.id)
                    
                    countries_count = file_len(MEDIA_ROOT + "default_countries.csv")
                    committees_count = file_len(MEDIA_ROOT + "default_committees.csv")
                    
                    self.assertTrue(committees_count > 0)
                    self.assertTrue(countries_count > 0)
                    
                    self.assertEquals(Committee.objects.filter(conference=conference).count(), committees_count)
                    self.assertEquals(Country.objects.filter(conference=conference).count(), countries_count)
                else:
                    self.assertTemplateUsed(response, 'conference/create-conference.html')
                    self.assertContains(response, "You do not have access to this page")
            else:
                self.assertRedirects(response, settings.LOGIN_URL + '?next=/new-conference/')
        
        # try creating duplicate conference
        conference_name = conferences[0].lower()
        secretariat_user = secretariat1
        conf_dict = {'name': conference_name,
                       'start_date': conference_date_1.strftime("%m/%d/%Y"),
                       'end_date': conference_date_2.strftime("%m/%d/%Y"),
                       'location':  conference_name + " Location",
                       'email_address' : secretariat_user['username'] + '@test.com',
                       'website_url' : 'http://www.google.com',
                       'organization_name' : conference_name + ", Inc",
                       'address_line_1' : '1 ' + conference_name  + " Lane",
                       'address_line_2' : "Mailbox A",
                       'city' : 'Austin',
                       'state' : 'TX',
                       'zip' : '77777',
                       'address_country' : 'USA'}
        
        response = self.client.post('/new-conference/', conf_dict, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        if self.is_logged_in():
            self.assertTemplateUsed(response, 'conference/create-conference.html')
            if self.is_staff_client():
                self.assertContains(response, "Conference Information")
                self.assertFormError(response, 'conference_form', 'name', 
                                     'Conference name already exists. <a href="/'+slugify(conference_name)+'/">Click here</a> to see this conference.')
            else:
                self.assertContains(response, "You do not have access to this page")
        else:
            self.assertRedirects(response, settings.LOGIN_URL + '?next=/new-conference/')
            
class CreateSchoolTest(LoginTestCase):
    def test_create_school(self):
        self.assertFalse(settings.ENABLE_CAPTCHA)
        if self.username is not None:
            self.client.login(username=self.username, password=self.password)
            
        for conference_name in conferences:
            new_school_url = '/' + slugify(conference_name) + '/new-school/'
            conference = Conference.objects.get(name=conference_name)
            
            if self.is_sponsor_client():
                # only attempt to register schools for this conference
                for school_name in schools_by_conference[conference_name]:
                    if self._user_data() in users_sponsors_by_school[school_name]:
                        school_exists = True
                        try:
                            school = School.objects.get(name=school_name)
                            school.conferences.get(id=conference.id)
                        except School.DoesNotExist:
                            school_exists = False
                        except Conference.DoesNotExist:
                            pass
                        
                        school_dict = {'school_name': school_name,
                                       'school_address_line_1': school_name + " Lane",
                                       'school_address_line_2': "",
                                       'school_city':  school_name + " Location",
                                       'school_state' : "TX",
                                       'school_zip' : '77777',
                                       'school_address_country' : "USA"}
                        user_dict = {'sponsor_username' : self.username,
                                     'sponsor_password' : self.password,
                                     'password2' : self.password,
                                     'sponsor_first_name' : self.username + first_name,
                                     'sponsor_last_name'  : self.username + last_name,
                                     'sponsor_email' : self.username + "@test.com",
                                     'sponsor_phone' : "555-555-5555"}
                        
                        response = self.client.get(new_school_url, follow=True)
                        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                        
                        school_admin_url = "/" + slugify(conference_name) + "/" + slugify(school_name) + "/"
                        school_index_url = '/school/' + slugify(school_name) + '/'
                        add_me_url = school_admin_url + "add-me"

                        # user already exists
                        if self.is_logged_in():
                            # Does this have a sponsor user object attached yet?
                            sponsor_obj_exists = True
                            try:
                                user = User.objects.get(username=self.username)
                                self.assertTrue(user.faculty_sponsor.school.name == school_name)
                            except ObjectDoesNotExist:
                                sponsor_obj_exists = False
                            
                            if school_exists:
                                if sponsor_obj_exists:
                                    # sponsor should be automatically registered for conference
                                    self.assertRedirects(response, school_admin_url)
                                    self.assertTemplateUsed(response, 'school/index.html')
                                    self.assertNotContains(response, "You do not have access to this page.")
                                else:
                                    # should get error that school already exists - need to enter access code to get permissions
                                    self.assertContains(response, "School Information")
                                    self.assertNotContains(response, "Faculty Sponsor Information")
                                    response = self.client.post(new_school_url, school_dict)
                                    self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                    self.assertTemplateUsed(response, 'register-new-school.html')
                                    self.assertFormError(response, 'school_form', 'school_name', 
                                                         'School name already exists. <a href="/school/'+slugify(school_name)+'/">Click here</a> to see this school.')
                                    
                                    response = self.client.get(school_index_url, follow=True)
                                    self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                    self.assertTemplateUsed(response, 'school_detail.html')
                                    self.assertContains(response, "You do not have access to this page.")
                                    self.assertContains(response, "grant-school-access")
                                    
                                    access_code_dict = {'access_code' : school.access_code,
                                                        'next' : school_index_url}
                                    response = self.client.post(school_index_url + 'grant-school-access', access_code_dict, follow=True)
                                    self.assertRedirects(response, school_index_url)
                                    self.assertContains(response, school_admin_url)
                                    self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                    self.assertTemplateUsed(response, 'school_detail.html')
                                    
                                    # sponsor object should exist now, but not registered for conference
                                    user = User.objects.get(username=self.username)
                                    self.assertTrue(user.faculty_sponsor.school.name == school_name)
                                    self.assertEqual(user.faculty_sponsor.conferences.filter(id=conference.id).count(), 0)
                                    
                                    response = self.client.get(school_admin_url, follow=True)
                                    self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                    self.assertTemplateUsed(response, 'school/index.html')
                                    self.assertNotContains(response, "You do not have access to this page.")
                                    self.assertContains(response, "add-me")
                                    
                                    response = self.client.get(add_me_url, follow=True)
                                    self.assertRedirects(response, school_admin_url)
                                    self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                    self.assertTemplateUsed(response, 'school/index.html')
                            else:
                                # create the school
                                self.assertContains(response, "School Information")
                                self.assertNotContains(response, "Faculty Sponsor Information")
                                response = self.client.post(new_school_url, school_dict, follow=True)
                                self.assertRedirects(response, school_admin_url)
                                self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                self.assertTemplateUsed(response, 'school/index.html')
                                self.assertNotContains(response, "You do not have access to this page.")
                        else:
                            self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                            self.assertTemplateUsed(response, 'register-new-school.html')
                            self.assertContains(response, "School Information")
                            self.assertContains(response, "Faculty Sponsor Information")
                            
                            response = self.client.post(new_school_url, dict(school_dict.items() + user_dict.items()), follow=True)
                            self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                            
                            if school_exists:
                                # create user and register with school and conference
                                self.assertTemplateUsed(response, 'register-new-school.html')
                                self.assertFormError(response, 'school_form', 'school_name', 
                                                         'School name already exists. <a href="/school/'+slugify(school_name)+'/">Click here</a> to see this school.')
                                
                                response = self.client.get(school_index_url, follow=True)
                                self.assertRedirects(response, settings.LOGIN_URL + '?next=' + school_index_url)
                                self.assertContains(response, "/accounts/register/")
                                
                                self.email = self.username + "@test.com"
                                response = self.client.post('/accounts/register/', 
                                                            {'username' : self.username,
                                                             'password1' : self.password,
                                                             'password2' : self.password,
                                                             'first_name' : self.username + first_name,
                                                             'last_name' : self.username + last_name,
                                                             'email' : self.email}, follow=True)
                                self.assertRedirects(response, settings.LOGIN_URL)
                                self.assertTrue(self.client.login(username=self.username, password=self.password))
                                
                                response = self.client.get(school_index_url, follow=True)
                                self.assertContains(response, "You do not have access to this page.")
                                self.assertContains(response, "grant-school-access")
                                self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                self.assertTemplateUsed(response, 'school_detail.html')
                                
                                access_code_dict = {'access_code' : school.access_code,
                                                    'next' : school_index_url}
                                response = self.client.post(school_index_url + 'grant-school-access', access_code_dict, follow=True)
                                self.assertRedirects(response, school_index_url)
                                self.assertContains(response, school_admin_url)
                                self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                self.assertTemplateUsed(response, 'school_detail.html')
                                
                                # sponsor object should exist now, but not registered for conference
                                user = User.objects.get(username=self.username)
                                self.assertTrue(user.faculty_sponsor.school.name == school_name)
                                self.assertEqual(user.faculty_sponsor.conferences.filter(id=conference.id).count(), 0)
                                
                                response = self.client.get(school_admin_url, follow=True)
                                self.assertNotContains(response, "You do not have access to this page.")
                                self.assertContains(response, "add-me")
                                self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                self.assertTemplateUsed(response, 'school/index.html')
                                
                                response = self.client.get(add_me_url, follow=True)
                                self.assertRedirects(response, school_admin_url)
                                self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                self.assertTemplateUsed(response, 'school/index.html')
                            else:
                                # create the user and the school
                                self.assertRedirects(response, settings.LOGIN_URL + '?next=' + school_admin_url)
                                
                                self.assertTrue(self.client.login(username=self.username, password=self.password))
                                response = self.client.get(school_admin_url, follow=True)
                                self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                                self.assertTemplateUsed(response, 'school/index.html')
                                self.assertNotContains(response, "You do not have access to this page.")
                        
                        # school and faculty sponsor are registered for conference
                        school = School.objects.get(name=school_name)
                        school.conferences.get(id=conference.id)
                        
                        user = User.objects.get(username=self.username)
                        self.assertTrue(user.faculty_sponsor.school.name == school_name)
                        user.faculty_sponsor.conferences.get(id=conference.id)
                        
                        response = self.client.get(school_admin_url, follow=True)
                        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                        self.assertTemplateUsed(response, 'school/index.html')
                        self.assertNotContains(response, "You do not have access to this page.")
                        
                        # remove some sponsors from some conferences
                        if self._user_data() not in users_sponsors_by_conference[conference_name]:
                            response = self.client.post(school_admin_url + 'ajax/remove-sponsor-from-conference', 
                                                        {'sponsor_pk':user.faculty_sponsor.pk}, follow=True)
                            self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                            self.assertContains(response, '"success": "true"', msg_prefix=str(response))
                            
                            user = User.objects.get(username=self.username)
                            self.assertTrue(user.faculty_sponsor.school.name == school_name)
                            self.assertEqual(user.faculty_sponsor.conferences.filter(id=conference.id).count(), 0)
                            
            elif self.is_secretariat_client() or self.is_staff_client():
                # secretariat and staff can't register schools
                response = self.client.get(new_school_url, follow=True)
                self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                self.assertTemplateUsed(response, 'register-new-school.html')
                self.assertContains(response, "You cannot create a new school as a staff member.")
            elif not self.is_logged_in():
                # anonymous request
                response = self.client.get(new_school_url, follow=True)
                self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                self.assertTemplateUsed(response, 'register-new-school.html')
                self.assertContains(response, "School Information")
                self.assertContains(response, "Faculty Sponsor Information")
                
class ConfigureRegistrationTest(LoginTestCase):
    def test_registration_configuration(self):
        if self.username is not None:
            self.client.login(username=self.username, password=self.password)
            
        if self.is_secretariat_client():
            self.conference_name = ""
            for conference in conferences:
                if secretariat_by_conference[conference] == self._user_data():
                    self.conference_name = conference
                    break
            
            self.assertNotEqual(len(self.conference_name), 0)
            self.conference_url = '/' + slugify(self.conference_name)
            self.conference_obj = Conference.objects.get(name=self.conference_name)
            
            # configure registration
            self.configure_conference()
            self.configure_committees()
            self.configure_countries()
            self.configure_fees()
            self.configure_delegate_positions()
    
    def configure_conference(self):
        # Save conference form
        conference_date_1 = datetime.date.today() + datetime.timedelta(3*365/12)
        conference_date_2 = conference_date_1 + datetime.timedelta(4)
        conference_date_3 = conference_date_1 - datetime.timedelta(4)
        new_location = self.conference_obj.location + " Street"
        form_dict = {'start_date':conference_date_1.strftime("%m/%d/%Y"),
                     'end_date':conference_date_2.strftime("%m/%d/%Y"),
                     'location':new_location,
                     'website_url':self.conference_obj.website_url,
                     'no_refunds_start_date':conference_date_3.strftime("%m/%d/%Y")}
        
        response = self.client.post(self.conference_url+'/secretariat/ajax/save-basic-conference-form', form_dict, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertNotContains(response, "form")
        response_json_dict = json.loads(response.content)
        self.assertTrue(response_json_dict.has_key('conference'))
        self.assertEqual(response_json_dict['conference'], self.conference_obj.pk)
    
        self.conference_obj = Conference.objects.get(name=self.conference_name)
        self.assertEqual(self.conference_obj.start_date, conference_date_1)
        self.assertEqual(self.conference_obj.end_date, conference_date_2)
        self.assertEqual(self.conference_obj.no_refunds_start_date, conference_date_3)
        self.assertEqual(self.conference_obj.location, new_location)

        # Get conference form
        response = self.client.get(self.conference_url+'/secretariat/ajax/get-basic-conference-form', follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertContains(response, "form")
        response_json_dict = json.loads(response.content)
        self.assertTrue(response_json_dict.has_key('form'))
        self.assertNotEqual(0, len(response_json_dict['form']))
        self.assertContains(response, conference_date_1.strftime("%Y-%m-%d"))
        self.assertContains(response, conference_date_2.strftime("%Y-%m-%d"))
        self.assertContains(response, conference_date_3.strftime("%Y-%m-%d"))
        self.assertContains(response, self.conference_obj.website_url)
    
    def configure_fees(self):
        # /conference/secretariat/ajax/get-conference-fees
        # /conference/secretariat/ajax/remove-fee
        # /conference/secretariat/ajax/add-fee
        # /conference/secretariat/ajax/get-conference-datepenalties
        # /conference/secretariat/ajax/remove-datepenalty
        # /conference/secretariat/ajax/add-datepenalty    
        pass
    
    def configure_committees(self):
        # Add new committee
        new_committee_dict = {'name': new_committee_name}
        response = self.client.post(self.conference_url+'/secretariat/ajax/add-committee', new_committee_dict, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertNotContains(response, "form")
        response_json_dict = json.loads(response.content)
        self.assertTrue(response_json_dict.has_key('pk'))
        new_committee_pk = response_json_dict['pk']
        self.assertTrue(response_json_dict.has_key('name'))
        self.assertEquals(new_committee_name, response_json_dict['name'])
        new_committee = Committee.objects.get(id=new_committee_pk)
        self.assertEquals(new_committee_name, new_committee.name)
        self.assertEqual(new_committee.conference, self.conference_obj)
        
        # /conference/secretariat/ajax/edit-committee
        edited_committee_name = new_committee_name + "123"
        edit_committee_dict = {'id': "name_" + str(new_committee_pk),
                               'value' : edited_committee_name}
        response = self.client.post(self.conference_url+'/secretariat/ajax/edit-committee', edit_committee_dict, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertEqual(response.content.decode('utf-8'), edited_committee_name)
        edited_committee = Committee.objects.get(id=new_committee_pk)
        self.assertEquals(edited_committee_name, edited_committee.name)
        self.assertEqual(edited_committee.conference, self.conference_obj)
        
        # Get conference committees
        response = self.client.get(self.conference_url+'/secretariat/ajax/get-conference-committees', follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        response_json_dict = json.loads(response.content)
        self.assertTrue(response_json_dict.has_key('form'))
        self.assertTrue(response_json_dict.has_key('objects'))
        for committee_dict in json.loads(response_json_dict['objects']):
            self.assertTrue(committee_dict.has_key('pk'))
            self.assertTrue(committee_dict.has_key('fields'))
            committee_fields = committee_dict['fields']
            self.assertTrue(committee_fields.has_key('name'))
            self.assertEqual(committee_dict['pk'], Committee.objects.get(name=committee_fields['name'], conference__name=self.conference_name).pk)
        self.assertContains(response, new_committee_pk)
        
        # Remove committee
        remove_committee_dict = {'pk': new_committee_pk}
        response = self.client.post(self.conference_url+'/secretariat/ajax/remove-committee', remove_committee_dict, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        response_json_dict = json.loads(response.content)
        self.assertTrue(response_json_dict.has_key('pk'))
        self.assertEqual(int(response_json_dict['pk']), new_committee_pk)
        self.assertRaises(Committee.DoesNotExist, Committee.objects.get, id=new_committee_pk)
        self.assertRaises(Committee.DoesNotExist, Committee.objects.get, name=edited_committee_name,conference__name=self.conference_name)
    
    def configure_countries(self):
        # Add new country
        new_country_dict = {'name': new_country_name, 'country_code': new_country_code}
        response = self.client.post(self.conference_url+'/secretariat/ajax/add-country', new_country_dict, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertNotContains(response, "form")
        response_json_dict = json.loads(response.content)
        self.assertTrue(response_json_dict.has_key('pk'))
        new_country_pk = response_json_dict['pk']
        self.assertTrue(response_json_dict.has_key('fields'))
        response_json_dict = response_json_dict['fields']
        self.assertTrue(response_json_dict.has_key('name'), msg=response_json_dict.keys())
        self.assertEquals(new_country_name, response_json_dict['name'])
        self.assertTrue(response_json_dict.has_key('country_code'))
        self.assertEquals(new_country_code, response_json_dict['country_code'])
        new_country = Country.objects.get(id=new_country_pk)
        self.assertEquals(new_country_name, new_country.name)
        self.assertEquals(new_country_code, new_country.country_code)
        self.assertEqual(new_country.conference, self.conference_obj)
        
        # /conference/secretariat/ajax/edit-country
        edited_country_name = new_country_name + "123"
        edit_country_dict = {'id': "name_" + str(new_country_pk),
                               'value' : edited_country_name}
        response = self.client.post(self.conference_url+'/secretariat/ajax/edit-country', edit_country_dict, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertEqual(response.content.decode('utf-8'), edited_country_name)
        edited_country = Country.objects.get(id=new_country_pk)
        self.assertEquals(edited_country_name, edited_country.name)
        self.assertEqual(edited_country.conference, self.conference_obj)
        
        # Get conference countries
        response = self.client.get(self.conference_url+'/secretariat/ajax/get-conference-countries', follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        response_json_dict = json.loads(response.content)
        self.assertTrue(response_json_dict.has_key('form'))
        self.assertTrue(response_json_dict.has_key('objects'))
        for country_dict in json.loads(response_json_dict['objects']):
            self.assertTrue(country_dict.has_key('pk'))
            self.assertTrue(country_dict.has_key('fields'))
            country_fields = country_dict['fields']
            self.assertTrue(country_fields.has_key('name'))
            self.assertTrue(country_fields.has_key('country_code'))
            self.assertEqual(country_dict['pk'], Country.objects.get(name=country_fields['name'], conference__name=self.conference_name).pk)
        self.assertContains(response, new_country_pk)
        self.assertContains(response, new_country_code)
        
        # Remove country
        remove_country_dict = {'pk': new_country_pk}
        response = self.client.post(self.conference_url+'/secretariat/ajax/remove-country', remove_country_dict, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        response_json_dict = json.loads(response.content)
        self.assertTrue(response_json_dict.has_key('pk'))
        self.assertEqual(int(response_json_dict['pk']), new_country_pk)
        self.assertRaises(Country.DoesNotExist, Country.objects.get, id=new_country_pk)
        self.assertRaises(Country.DoesNotExist, Country.objects.get, name=edited_country_name,conference__name=self.conference_name)
    
    def configure_delegate_positions(self):
        # /conference/secretariat/ajax/get-delegate-positions-table
        # /conference/secretariat/ajax/get-delegate-positions
        # /conference/secretariat/ajax/get-individual-delegate-positions
        # /conference/secretariat/ajax/upload-delegate-positions
        # /conference/secretariat/ajax/set-delegate-position-count
        # /conference/secretariat/ajax/set-delegate-positions
        # /conference/secretariat/ajax/set-individual-delegate-positions
        # /conference/secretariat/ajax/remove-delegate-position
        # /conference/secretariat/ajax/add-delegate-position
        pass
    
class SchoolRegistrationTest(LoginTestCase):
    def test_school_registration(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
        
        # /conference/school/ajax/get-school-mailing-address-form
        # /conference/school/ajax/save-school-mailing-address-form
        # /conference/school/ajax/get-edit-sponsor-form
        # /conference/school/ajax/save-edit-sponsor-form
        # /conference/school/ajax/remove-sponsor-from-school
        # /conference/school/ajax/remove-sponsor-from-conference
        # /conference/school/ajax/add-sponsor-to-conference
    
    def test_submit_country_preferences(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
        
        # /conference/school/ajax/get-country-preferences
        # /conference/school/ajax/set-country-preferences
        # /conference/school/ajax/get-country-preferences-html-ajax
    
class CountryAssignmentTest(LoginTestCase):
    def test_country_assignments(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
        
        # /conference/secretariat/ajax/get-country-school-assignments
        # /conference/secretariat/ajax/set-country-school-assignments
        # /conference/secretariat/ajax/upload-school-country-assignments
    
class DelegateRegistrationTest(LoginTestCase):
    def test_delegate_registration(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
            
        # /conference/school/ajax/edit-delegate
        # /conference/school/ajax/get-edit-delegate-form
        # /conference/school/ajax/remove-delegate
    
class PaymentsTest(LoginTestCase):
    def test_payments(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
        
        # /conference/secretariat/ajax/get-conference-payments
        # /conference/secretariat/ajax/edit-payment
        # /conference/secretariat/ajax/remove-payment
        # /conference/secretariat/ajax/add-payment
    