#!/usr/bin/env python
import unittest

from bs4 import BeautifulSoup
import re, requests, time

from httmock import response, all_requests, urlmatch, HTTMock

from unittest import TestCase
from datasift import DataSiftClient, DataSiftConfig
from datasift.exceptions import DataSiftApiException, DataSiftApiFailure, AuthException
from requests import HTTPError

from tests.mocks import *

# Helper methods
def get_all_gists_on_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    gist_js = soup.find_all("script", src=re.compile("gist"))
    gists = map(lambda x: x["src"].replace(".js", ""), gist_js)
    real_urls = map(lambda x:requests.get(x).url+"/raw", gists)
    data = map(lambda x: requests.get(x), real_urls)
    data = filter(lambda x:x.url.endswith(".json"), data)
    return data

def find_api_doc_of(function):
    if not hasattr(function, "__doc__"):
        return None
    docstring = function.__doc__
    devlinks = filter(lambda x:x.startswith("http://dev.datasift.com/docs"), docstring.split())
    for item in devlinks:
        return item

def mock_output_of(function):
    """ Takes a function and generates a mock suitable for use with it.

        Returns the mock function and the list of results to expect out, in order
    """
    documentation = find_api_doc_of(function)
    gists = get_all_gists_on_page(documentation)
    internal = gists.__iter__()
    @all_requests
    def mocked_response(url, content):
        return response(200, next(internal), {'content-type': 'application/json'}, None, 5, content)
    return mocked_response, gists

def assert_dict_structure(testcase, structure, data):
    for key in structure:
        testcase.assertIn(key, data)
        if key in data:
            assert_dict_structure(testcase, structure[key], data[key])

# TestCases

class TestMockedClient(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.client = DataSiftClient(DataSiftConfig("testuser", "testapikey"))

    def test_creation_of_client(self):
        self.assertTrue(self.client)

    def test_handling_of_authorization_failed(self):
        with HTTMock(authorization_failed):
            self.assertRaises(AuthException, self.client.balance)

    def test_output_of_balance(self):
        mock, expected = mock_output_of(self.client.balance)
        with HTTMock(mock):
            for expecteditem in expected:
                results = self.client.balance()
                assert_dict_structure(self, results, expecteditem)
                #self.assertDictEqual(item, self.client.balance())

    def test_compile_with_valid_output(self):
        mock, expected = mock_output_of(self.client.compile)
        with HTTMock(mock):
            for item in expected:
                self.assertDictEqual(item, self.client.compile("dummy csdl that is valid"))

    def test_compile_invalid_csdl(self):
        with HTTMock(failed_compilation_of_csdl):
            self.assertRaises(DataSiftApiException, self.client.compile, ("dummy csdl which is bad"))

    def test_is_valid_csdl(self):
        with HTTMock(failed_compilation_of_csdl):
            self.assertFalse(self.client.is_valid("dummy csdl which is bad"))

        mock, expected = mock_output_of(self.client.validate)
        with HTTMock(mock):
            for item in expected:
                self.assertTrue(self.client.is_valid("dummy csdl which is valid"))

    def test_error_handling_of_internal_server_errors(self):
        with HTTMock(internal_server_error):
            self.assertRaises(DataSiftApiFailure, self.client.balance)

    def test_error_handling_of_weird_errors(self):
        with HTTMock(weird_error):
            self.assertRaises(HTTPError, self.client.validate, ("csdl which turns into a teapot"))

    def test_historics_prepare(self):
        mock, expected = mock_output_of(self.client.historics.prepare)
        with HTTMock(mock):
            for expected_output in expected:
                results = self.client.historics.prepare("fake csdl hash", int(time.time()-60), int(time.time()), "my fake historics query", ["twitter"], sample=10)
                assert_dict_structure(self, results, expected_output)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMockedClient)
    unittest.TextTestRunner(verbosity=2).run(suite)
