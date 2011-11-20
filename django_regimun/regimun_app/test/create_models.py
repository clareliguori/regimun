from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from regimun_app.test.login import LoginTestCase
import settings

class AccountManagementTest(LoginTestCase):
    def test_create_user(self):
        
        response = self.client.get('/')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertTemplateUsed(response, 'conference_list.html')
        
        # get the registration form
        response = self.client.get('/accounts/register/')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, "First name", status_code=200)

        if self.username is None:
            return
                
        user_exists = True
        try:
            User.objects.get(username=self.username)
        except User.DoesNotExist:
            user_exists = False
        except MultipleObjectsReturned:
            self.fail("Multiple users with same username " + self.username)
        
        # submit the registration form
        response = self.client.post('/accounts/register/', 
                                    {'username' : self.username,
                                     'password1' : self.password,
                                     'password2' : self.password,
                                     'first_name' : self.username + " First",
                                     'last_name' : self.username + " Last",
                                     'email' : self.username + "@test.com"}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        
        if user_exists:
            # should give an error
            self.assertTemplateUsed(response, 'accounts/register.html')
            self.assertContains(response, "A user with that username already exists.")
        else:
            # should redirect to login view
            self.assertRedirects(response, settings.LOGIN_URL)
        
        # try to login
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': self.password}, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertRedirects(response, '/')
        self.assertTrue('_auth_user_id' in self.client.session)
        
class CreateConferenceTest(LoginTestCase):
    def test_create_conference(self):
        response = self.client.get('/')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertTemplateUsed(response, 'conference_list.html')
