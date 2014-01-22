
import unittest

from bs4 import BeautifulSoup
import re, requests

from httmock import response, all_requests, urlmatch, HTTMock

from unittest import TestCase
from datasift import DataSiftClient
from datasift import DataSiftConfig
from datasift.exceptions import DataSiftApiException


def get_all_gists_on_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    gist_js = soup.find_all("script", src=re.compile("gist"))
    gists = map(lambda x: x["src"].replace(".js", ""), gist_js)
    real_urls = map(lambda x:requests.get(x).url+"/raw", gists)
    data = map(lambda x: requests.get(x).json(), real_urls)
    return data

def find_api_doc_of(function):
    if not hasattr(function, "__doc__"):
        return None
    docstring = function.__doc__
    devlinks = filter(lambda x:x.startswith("http://dev.datasift.com/docs"), docstring.split())
    return devlinks[0]

def mock_output_of(function):
    documentation = find_api_doc_of(function)
    gists = get_all_gists_on_page(documentation)

    internal = gists.__iter__()

    @all_requests
    def mocked_response(url, content):
        return response(200, internal.next(), {'content-type': 'application/json'}, None, 5, content)

    return mocked_response, gists

class ClientTests(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.client = DataSiftClient(DataSiftConfig("testuser", "testapikey"))

    def test_creation_of_client_with_bad_credentials(self):
        self.assertTrue(self.client)

    def test_handling_of_bad_credentials(self):
        with HTTMock(all_requests(lambda u, c: response(403, {"error": "Authorization failed)"}, {'content-type': 'application/json'}, None, 5, c))):
            self.assertRaises(DataSiftApiException, self.client.balance)

    def test_output_of_balance(self):
        mock, expected = mock_output_of(self.client.balance)
        with HTTMock(mock):
            for item in expected:
                self.assertDictEqual(item, self.client.balance())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ClientTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
