from regimun_app.test.accounts import AccountManagementTest
from regimun_app.test.conference_views import ConferenceTest
from regimun_app.test.create_models import *
from regimun_app.test.login import LoginTestCase
from regimun_app.test.test_data import *
from unittest import TestSuite

from django.conf import settings

def suite():
    users = [user_staff, user_staff, user_none] + users_sponsors + users_secretariat
    settings.ENABLE_CAPTCHA = False
    settings.TEMPLATE_STRING_IF_INVALID = "BAD TEMPLATE"
    
    suite = TestSuite()
    suite.addTests(LoginTestCase.parametrize(AccountManagementTest, [user_staff, user_staff, user_none]))
    suite.addTests(LoginTestCase.parametrize(CreateConferenceTest, [user_staff, user_none]))
    suite.addTests(LoginTestCase.parametrize(AccountManagementTest, [sponsor1, sponsor2, sponsor3, sponsor4]))
    #suite.addTests(LoginTestCase.parametrize(CreateSchoolTest, users))
    suite.addTests(LoginTestCase.parametrize(AccountManagementTest, users_secretariat + users_sponsors))
    #suite.addTests(LoginTestCase.parametrize(ConferenceTest, users))
    suite.addTests(LoginTestCase.parametrize(ConfigureRegistrationTest, users))
    #suite.addTests(LoginTestCase.parametrize(SchoolRegistrationTest, users))
    #suite.addTests(LoginTestCase.parametrize(CountryAssignmentTest, users))
    #suite.addTests(LoginTestCase.parametrize(DelegateRegistrationTest, users))
    #suite.addTests(LoginTestCase.parametrize(PaymentsTest, users))
    #suite.addTests(LoginTestCase.parametrize(ConferenceTest, users))
    return suite
