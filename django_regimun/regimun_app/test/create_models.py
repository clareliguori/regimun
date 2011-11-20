from django.contrib.auth.models import User
from django.core import mail
from django.core.exceptions import MultipleObjectsReturned
from regimun_app.test.login import LoginTestCase
import re
import settings

class AccountManagementTest(LoginTestCase):
    def test_create_user(self):
        self.assertFalse('_auth_user_id' in self.client.session)
        
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
        password1 = "password1"
        password2 = "password2"
        email = self.username + "@test.com"
        response = self.client.post('/accounts/register/', 
                                    {'username' : self.username,
                                     'password1' : password1,
                                     'password2' : password1,
                                     'first_name' : self.username + " First",
                                     'last_name' : self.username + " Last",
                                     'email' : email}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        
        if user_exists:
            # should give an error
            self.assertTemplateUsed(response, 'accounts/register.html')
            self.assertFormError(response, 'form', 'username', "A user with that username already exists.")
            password1 = self.password
        else:
            # should redirect to login view
            self.assertRedirects(response, settings.LOGIN_URL)
        
        # try to login
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': password1}, follow=True)
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertRedirects(response, '/')
        
        # logout
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertRedirects(response, settings.LOGIN_URL)
        
        # change password
        response = self.client.get('/accounts/change_password/', follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertRedirects(response, settings.LOGIN_URL + '?next=/accounts/change_password/')
        
        self.assertTrue(self.client.login(username=self.username, password=password1))
        response = self.client.get('/accounts/change_password/')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertContains(response, self.username)
        self.assertTemplateUsed(response, 'accounts/password_change_form.html')
        
        # empty fields
        response = self.client.post('/accounts/change_password/')
        self.assertTemplateUsed(response, 'accounts/password_change_form.html')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertFormError(response, 'form', 'old_password', "This field is required.")
        self.assertFormError(response, 'form', 'new_password1', "This field is required.")
        self.assertFormError(response, 'form', 'new_password2', "This field is required.")
        
        # wrong old password
        response = self.client.post('/accounts/change_password/', {'old_password': "hello",
                                                                   'new_password1': password2,
                                                                   'new_password2': password2})
        self.assertTemplateUsed(response, 'accounts/password_change_form.html')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertFormError(response, 'form', 'old_password', "Your old password was entered incorrectly. Please enter it again.")
        
        # non-matching new passwords
        response = self.client.post('/accounts/change_password/', {'old_password': password1,
                                                                   'new_password1': password2,
                                                                   'new_password2': "hello"})
        self.assertTemplateUsed(response, 'accounts/password_change_form.html')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertFormError(response, 'form', 'new_password2', "The two password fields didn't match.")
        
        # change password successfully
        response = self.client.post('/accounts/change_password/', {'old_password': password1,
                                                                   'new_password1': password2,
                                                                   'new_password2': password2}, 
                                                                   follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertRedirects(response, '/accounts/password_changed/')
        self.assertTemplateUsed(response, 'accounts/password_change_done.html')
        self.assertTrue('_auth_user_id' in self.client.session)

        # log in with new password
        self.client.logout()
        self.assertTrue(self.client.login(username=self.username, password=password2))
        self.client.logout()
        self.assertFalse('_auth_user_id' in self.client.session)
        
        # reset password
        response = self.client.get('/accounts/request_password_reset/')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertTemplateUsed(response, 'accounts/password_reset_form.html')
        
        # empty fields
        response = self.client.post('/accounts/request_password_reset/')
        self.assertTemplateUsed(response, 'accounts/password_reset_form.html')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertFormError(response, 'form', 'email', "This field is required.")

        # invalid email address
        response = self.client.post('/accounts/request_password_reset/', {'email' : 'hello'})
        self.assertTemplateUsed(response, 'accounts/password_reset_form.html')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertFormError(response, 'form', 'email', "Enter a valid e-mail address.")

        # invalid email address
        response = self.client.post('/accounts/request_password_reset/', {'email' : 'hello@hello.com'})
        self.assertTemplateUsed(response, 'accounts/password_reset_form.html')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertFormError(response, 'form', 'email', "That e-mail address doesn't have an associated user account. Are you sure you've registered?")

        # successful request
        response = self.client.post('/accounts/request_password_reset/', {'email' : email}, follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertRedirects(response, '/accounts/password_reset_requested/')
        self.assertTemplateUsed(response, 'accounts/password_reset_done.html')
        
        # verify the reset email        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to.index(email), 0)

        # find the reset link
        p = re.compile("^http.*$", re.MULTILINE)
        link = p.search(mail.outbox[0].body).group()
        response = self.client.get(link)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertTemplateUsed(response, 'accounts/password_reset_confirm.html')
        self.assertContains(response, "Enter New Password")
        
        response = self.client.post(link, {'new_password1': self.password,
                                          'new_password2': self.password}, 
                                          follow=True)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertRedirects(response, '/accounts/password_reset/password_reset_complete/')
        self.assertTemplateUsed(response, 'accounts/password_reset_complete.html')
        self.assertContains(response, settings.LOGIN_URL)
        
        # try to login with the new password
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        self.client.logout()
        
class CreateConferenceTest(LoginTestCase):
    def test_create_conference(self):
        response = self.client.get('/')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertTemplateUsed(response, 'conference_list.html')
