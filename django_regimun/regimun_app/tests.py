from regimun_app.test.conference_views import ConferenceTest
from regimun_app.test.create_models import AccountManagementTest
from regimun_app.test.login import LoginTestCase
from unittest import TestSuite

def suite():
    suite = TestSuite()
    suite.addTests(LoginTestCase.parametrize(AccountManagementTest))
    suite.addTests(LoginTestCase.parametrize(ConferenceTest))
    return suite
