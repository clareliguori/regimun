from django.template.defaultfilters import slugify
from regimun_app.test.login import LoginTestCase
from regimun_app.test.test_data import *

from django.conf import settings

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
    
    def test_secretariat_admin_page(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
            
        for conference_name in conferences:
            secretariat_url = '/' + slugify(conference_name) + "/secretariat/"
            response = self.client.get(secretariat_url, follow=True)
            self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
            
            if self.is_logged_in():
                self.assertTemplateUsed(response, 'secretariat/index.html')
                self.assertContains(response, conference_name)
                
                if self.is_secretariat_of_conference(conference_name) or self.is_staff_client():
                    for school_name in schools:
                        if school_name in schools_by_conference[conference_name]:
                            self.assertContains(response, school_name)
                        else:
                            self.assertNotContains(response, school_name)
                else:
                    self.assertContains(response, "You do not have access to this page.")
            else:
                self.assertRedirects(response, settings.LOGIN_URL + '?next=' + secretariat_url)
    
    def test_secretariat_school_view(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
            
        for conference_name in conferences:
            school_view_url  = '/' + slugify(conference_name) + '/secretariat/see-school'
            
            for school_name in schools:
                response = self.client.post(school_view_url, {'name' : school_name }, follow=True)
                
                if self.is_logged_in() and (self.is_staff_client() or self.is_secretariat_of_conference(conference_name)):
                    self.assertRedirects(response, '/' + slugify(conference_name) + '/' + slugify(school_name) + '/')
                    self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                    self.assertTemplateUsed(response, 'school/index.html')
                    self.assertContains(response, conference_name)
                    self.assertContains(response, school_name)
                    self.assertNotContains(response, "You do not have access to this page.")
                elif self.is_logged_in():
                    self.assertEquals(response.status_code, 404)
                else:
                    self.assertRedirects(response, settings.LOGIN_URL + '?next=' + school_view_url)
    
    def test_secretariat_downloads(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
        
        valid_spreadsheets = ['country-committee-assignments','school-country-assignments','sponsor-contacts','delegates','country-preferences','delegate-count-requests']
        
        for conference_name in conferences:
            # spreadsheet downloads
            conference_slug = slugify(conference_name)
            downloads_url  = '/' + conference_slug + '/secretariat/downloads/?'
            
            for spreadsheet in valid_spreadsheets:
                response = self.client.get(downloads_url + spreadsheet, follow=True)
                
                if self.is_logged_in() and (self.is_staff_client() or self.is_secretariat_of_conference(conference_name)):
                    self.assertEquals(response.status_code, 200)
                    self.assertEquals(response['Content-Type'], 'text/csv')
                    self.assertEquals(response['Content-Disposition'], 'attachment; filename=' + spreadsheet + '-' + conference_slug + ".csv")
                elif self.is_logged_in():
                    self.assertEquals(response.status_code, 404)
            
            # invalid download URLs
            if self.is_logged_in():
                response = self.client.get(downloads_url + "aaaa", follow=True)
                self.assertEquals(response.status_code, 404)
                
                downloads_url  = '/' + conference_slug + '/secretariat/downloads/'
                response = self.client.get(downloads_url, follow=True)
                self.assertEquals(response.status_code, 404)
                
                response = self.client.post(downloads_url, follow=True)
                self.assertEquals(response.status_code, 404)
            
            # invoice downloads
            invoice_types = [{'url':'invoices', 'app_type':'pdf', 'file_ext':'pdf'},
                             {'url':'invoices-doc', 'app_type':'msword', 'file_ext':'doc'}]
            for invoice_type in invoice_types:
                invoices_url  = '/' + conference_slug + '/secretariat/' + invoice_type['url']
                response = self.client.get(invoices_url, follow=True)
                if self.is_logged_in() and (self.is_staff_client() or self.is_secretariat_of_conference(conference_name)):
                    self.assertEquals(response.status_code, 200)
                    self.assertEquals(response['Content-Type'], 'application/' + invoice_type['app_type'])
                    self.assertEquals(response['Content-Disposition'], 'attachment; filename=invoices-' + conference_slug + "." + invoice_type['file_ext'])
                elif self.is_logged_in():
                    self.assertEquals(response.status_code, 404)
            
    def test_school_downloads(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
            
        valid_spreadsheets = ['country-committee-assignments']
        
        for conference_name in conferences:
            conference_slug = slugify(conference_name)
                    
            for school_name in schools:
                school_slug = slugify(school_name)
                downloads_url  = '/' + conference_slug + '/' + school_slug + '/downloads/'
                for spreadsheet in valid_spreadsheets:
                    response = self.client.get(downloads_url + '?' + spreadsheet, follow=True)
                
                    if self.is_logged_in() and school_name in schools_by_conference[conference_name] and \
                        (self.is_staff_client() or self.is_secretariat_of_conference(conference_name) or self.is_sponsor_of_school(school_name)):
    
                        self.assertEquals(response.status_code, 200)
                        self.assertEquals(response['Content-Type'], 'text/csv')
                        self.assertEquals(response['Content-Disposition'], 'attachment; filename=' + spreadsheet + '-' + conference_slug + ".csv")
                    elif self.is_logged_in():
                        self.assertEquals(response.status_code, 404)
   
                # invalid download URLs
                if self.is_logged_in():
                    response = self.client.get(downloads_url + "?aaaa", follow=True)
                    self.assertEquals(response.status_code, 404)
                    
                    response = self.client.get(downloads_url, follow=True)
                    self.assertEquals(response.status_code, 404)
                    
                    response = self.client.post(downloads_url, follow=True)
                    self.assertEquals(response.status_code, 404)
   
                # invoice downloads
                invoice_types = [{'url':'invoice', 'app_type':'pdf', 'file_ext':'pdf'},
                                 {'url':'invoice-doc', 'app_type':'msword', 'file_ext':'doc'},
                                 {'url':'invoice-from-request', 'app_type':'pdf', 'file_ext':'pdf'},]
                for invoice_type in invoice_types:
                    invoices_url  = '/' + conference_slug + '/' + school_slug + '/' + invoice_type['url']
                    response = self.client.get(invoices_url, follow=True)
                    if self.is_logged_in() and school_name in schools_by_conference[conference_name] and \
                        (self.is_staff_client() or self.is_secretariat_of_conference(conference_name) or self.is_sponsor_of_school(school_name)):
                        self.assertEquals(response.status_code, 200)
                        self.assertEquals(response['Content-Type'], 'application/' + invoice_type['app_type'])
                        self.assertEquals(response['Content-Disposition'], 'attachment; filename=invoice-' + conference_slug + "-" + school_slug + "." + invoice_type['file_ext'])
                    elif self.is_logged_in():
                        self.assertEquals(response.status_code, 404)
   
    def test_school_admin_page(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
            
        for conference_name in conferences:
            for school_name in schools_by_conference[conference_name]:
                school_admin_url = '/' + slugify(conference_name) + '/' + slugify(school_name) + '/'
                response = self.client.get(school_admin_url, follow=True)
                
                self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
                
                if self.is_logged_in():
                    self.assertTemplateUsed(response, 'school/index.html')
                    self.assertContains(response, conference_name)
                    self.assertContains(response, school_name)
                    
                    if self.is_secretariat_of_conference(conference_name) or self.is_staff_client() or self.is_sponsor_of_school(school_name):
                        self.assertContains(response, "School Mailing Address")
                    else:
                        self.assertContains(response, "You do not have access to this page.")
                else:
                    self.assertRedirects(response, settings.LOGIN_URL + '?next=' + school_admin_url)
    
    def test_ajax(self):
        # TODO test security (only secretariat can access secretariat ajax, etc)
        pass
