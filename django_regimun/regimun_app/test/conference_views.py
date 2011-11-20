from regimun_app.test.login import LoginTestCase
import settings

class ConferenceTest(LoginTestCase):
    def test_conference_index(self):
        if not (self.username is None):
            self.assertTrue(self.client.login(username=self.username, password=self.password))
        response = self.client.get('/')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
        self.assertTemplateUsed(response, 'conference_list.html')
