from regimun_app.test.login import LoginTestCase
import settings

class ConferenceTest(LoginTestCase):
    def test_conference_index(self):
        if self.username is not None:
            self.assertTrue(self.client.login(username=self.username, password=self.password), msg='Failed to login ' + self.username + ', ' + self.password)
        response = self.client.get('/')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertTemplateUsed(response, 'conference_list.html')
