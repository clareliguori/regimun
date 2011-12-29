from django.test.client import Client
from django.test.testcases import TestCase
from regimun_app.test.test_data import *
from unittest import TestLoader

class LoginTestCase(TestCase):
    username = None
    password = None

    def __init__(self, methodName='runTest', client=None, username=None, password=None):
        super(LoginTestCase, self).__init__(methodName)
        self.client = client
        self.username = username
        self.password = password
    
    # Don't destroy the DB between test cases
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass 
    
    def _user_data(self):
        return {'username': self.username, 'password': self.password}
    
    def is_logged_in(self):
        return '_auth_user_id' in self.client.session
    
    def is_staff_client(self):
        return self._user_data() == user_staff
    
    def is_secretariat_client(self):
        return self._user_data() in users_secretariat
    
    def is_sponsor_client(self):
        return self._user_data() in users_sponsors
    
    def is_sponsor_of_school(self, school_name):
        return self.is_sponsor_client() and self._user_data() in users_sponsors_by_school[school_name]
    
    @staticmethod
    def parametrize(testcase_class, users):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'client'.
        """
        
        testloader = TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        tests = []
        for name in testnames:
            # Not logged in
            client = Client()
            tests.append(testcase_class(name, client=client))
            
            # Log in users
            for user in users:
                client = Client()
                tests.append(testcase_class(name, client=client, username=user['username'], password=user['password']))
        return tests

