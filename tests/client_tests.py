
import unittest

from unittest import TestCase
from datasift.exceptions import AuthException
import datasift.datasift_request as DataSiftClient


class ClientTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def test_not_providing_auth_should_raise_auth_exception(self):
        self.assertRaises(TypeError, DataSiftClient.req, 'compile')

    def test_providing_auth_doesnt_raise_auth_exception(self):
        #this should only fail if AuthException is raised
        DataSiftClient.req('compile', auth=('username', 'api_key'))

    def test_auth_username_cannot_be_empty(self):
        self.assertRaises(AuthException, DataSiftClient.req, 'compile', auth=('', 'api_key'))

    def test_auth_api_key_cant_be_empty(self):
        self.assertRaises(AuthException, DataSiftClient.req, 'compile', auth=('username', ''))

    def test_auth_length_must_be_2(self):
        self.assertRaises(AuthException, DataSiftClient.req, 'compile', auth=('username', 'api_key', 'anything'))

##todo at least two more tests of the request method testing it does post and get request, maybe using mock interface

if __name__ == '__main__':
    unittest.main()
