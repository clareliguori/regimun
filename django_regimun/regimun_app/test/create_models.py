from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from regimun_app.models import Conference, Committee, Country
from regimun_app.test.login import LoginTestCase
from regimun_app.test.test_data import *
import datetime
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
            if self.is_logged_in():
                if self.is_staff_client():
                    self.assertRedirects(response, '/' + slugify(conference_name) + '/secretariat/')
                    self.assertTemplateUsed(response, 'secretariat/index.html')
                    
                    # test that the secretariat user was created and conference object was created
                    secretariat_user = User.objects.get(username=secretariat_user['username'])
                    conference = Conference.objects.get(name=conference_name)
                    
                    secretariat_user.secretariat_member.conferences.get(id=conference.id)
                    
                    self.assertTrue(Committee.objects.filter(conference=conference).count() > 0)
                    self.assertTrue(Country.objects.filter(conference=conference).count() > 0)
                else:
                    self.assertTemplateUsed(response, 'conference/create-conference.html')
                    self.assertContains(response, "You do not have access to this page")
            else:
                self.assertRedirects(response, settings.LOGIN_URL + '?next=/new-conference/')
            
            