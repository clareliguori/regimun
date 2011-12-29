from django.template.defaultfilters import slugify
from regimun_app.test.login import LoginTestCase
from regimun_app.test.test_data import *
import settings

class ConferenceTest(LoginTestCase):
    def test_conference_index(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
        response = self.client.get('/')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertTemplateUsed(response, 'conference_list.html')

        for conference_name in conferences:
            self.assertContains(response, conference_name)
            self.assertContains(response, slugify(conference_name))
    
    def test_conference_school_index(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
        
        for conference_name in conferences:
            response = self.client.get('/' + slugify(conference_name), follow=True)
            self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
            self.assertTemplateUsed(response, 'conference_detail.html')
            self.assertContains(response, conference_name)
            
            for school_name in schools:
                if school_name in schools_by_conference[conference_name]:
                    self.assertContains(response, school_name)
                    self.assertContains(response, slugify(school_name))
                else:
                    self.assertNotContains(response, school_name)
                
    def test_school_index(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
        
        for school_name in schools:
            school_index_url = '/school/' + slugify(school_name) + "/"
            response = self.client.get(school_index_url, follow=True)
            self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
            
            if self.is_logged_in():
                if self.is_staff_client() or self.is_sponsor_of_school(school_name):
                    self.assertTemplateUsed(response, 'school_detail.html')
                    self.assertContains(response, school_name)
                    
                    for conference_name in conferences:
                        if school_name in schools_by_conference[conference_name]:
                            self.assertContains(response, conference_name)
                            self.assertContains(response, slugify(conference_name))
                        else:
                            self.assertNotContains(response, conference_name)
                            self.assertNotContains(response, slugify(conference_name))
                else:
                    self.assertContains(response, "You do not have access to this page.")
            else:
                self.assertRedirects(response, settings.LOGIN_URL + '?next=' + school_index_url)
                