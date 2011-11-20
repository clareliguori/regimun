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
    
    @staticmethod
    def parametrize(testcase_class):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'client'.
        """
        users = [user_staff, user_staff, secretariat1, secretariat2, user_none] + users_sponsors
        
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

