from regimun_app.test.accounts import AccountManagementTest
from regimun_app.test.conference_views import ConferenceTest
from regimun_app.test.create_models import CreateConferenceTest
from regimun_app.test.login import LoginTestCase
from regimun_app.test.test_data import *
from unittest import TestSuite

def suite():
    users = [user_staff, user_staff, user_none] + users_sponsors + users_secretariat
    
    suite = TestSuite()
    suite.addTests(LoginTestCase.parametrize(AccountManagementTest, [user_staff, user_staff, user_none]))
    suite.addTests(LoginTestCase.parametrize(CreateConferenceTest, [user_staff, user_none]))
    suite.addTests(LoginTestCase.parametrize(AccountManagementTest, users_secretariat + users_sponsors))
    suite.addTests(LoginTestCase.parametrize(ConferenceTest, users))
    return suite
