#!/usr/bin/env python
from __future__ import print_function
import sys, os

if sys.version_info < (2, 7):
    import unittest2 as unittest
    from unittest2 import TestCase
else:
    import unittest
    from unittest import TestCase

from bs4 import BeautifulSoup
import re, requests, time, json
from datetime import datetime

from httmock import response, all_requests, urlmatch, HTTMock

from datasift import DataSiftClient, DataSiftConfig
from datasift.exceptions import *
from requests import HTTPError
from requests.auth import HTTPBasicAuth

from tests.mocks import *

GITHUB_TOKEN=os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    sys.stderr.write("Please export a github OAUTH token as GITHUB_TOKEN to run these tests")
    sys.exit(1)

# Helper methods
def get_all_gists_on_page(url):
    r = requests.get(url)
    # find all gists
    soup = BeautifulSoup(r.content)
    gist_js = soup.find_all("script", src=re.compile("gist"))
    # grab the links and turn them into API links
    gists = map(lambda x: "https://api.github.com/gists/" + x["src"].replace(".js", "").split("/")[-1], gist_js)
    # pull the API links with our github key
    data = map(lambda x: requests.get(x+"?access_token="+GITHUB_TOKEN).json(), gists)
    # throw away entries that the API error'd n
    data = filter(lambda x: not (u"message" in x and x[u"message"] == u"Not Found"), data)
    # throw away non-JSON ones
    data = filter(lambda x:x[u"files"][list(x["files"].keys())[0]]["language"] == "JSON", data)
    # pull the actual JSON content
    results = []
    for item in data:
        try:
            r = json.loads(item[u"files"][list(item["files"].keys())[0]]["content"])
            results.append(r)
        except:
            pass
    # throw away examples of errors
    results = filter(lambda x:"error" not in x, results)
    return results

def find_api_doc_of(function):
    if not hasattr(function, "__doc__"):
        return None
    docstring = function.__doc__
    devlinks = filter(lambda x:x.startswith("http://dev.datasift.com/docs"), docstring.split())
    for item in devlinks:
        return item

def mock_output_of(function, prep=None):
    """ Takes a function and generates a mock suitable for use with it.

        Returns the mock function and the list of results to expect out, in order
    """
    documentation = find_api_doc_of(function)
    gists = list(get_all_gists_on_page(documentation))
    internal = gists.__iter__()

    @all_requests
    def mocked_response(url, content):
        data = next(internal)
        if prep:
            data = prep(data)
        return response(200, data, {'content-type': 'application/json'}, None, 5, content)
    return mocked_response, list(gists)

def assert_dict_structure(testcase, structure, data):
    for key in structure:
        assert (key in data)
        if key in data:
            if isinstance(key, dict):
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
            runs = 0
            for expecteditem in expected:
                runs += 1
                results = self.client.balance()
                assert_dict_structure(self, results, expecteditem)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_compile_raw_output(self):
        mock, expected = mock_output_of(self.client.compile)
        with HTTMock(mock):
            runs = 0
            for item in expected:
                runs += 1
                assert_dict_structure(self, item, self.client.compile("dummy csdl that is valid").raw)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_compile_python_friendly_output(self):
        mock, expected = mock_output_of(self.client.compile)
        with HTTMock(mock):
            runs = 0
            for item in expected:
                runs += 1
                result = self.client.compile("dummy csdl that is valid")
                assert_dict_structure(self, item, result.raw)
                assert_dict_structure(self, item, result)
                self.assertEqual(result["created_at"], datetime.strptime(result.raw["created_at"], "%Y-%m-%d %H:%M:%S"))
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_compile_with_valid_output(self):
        mock, expected = mock_output_of(self.client.compile)
        with HTTMock(mock):
            runs = 0
            for item in expected:
                runs += 1
                assert_dict_structure(self, item, self.client.compile("dummy csdl that is valid"))
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_compile_invalid_csdl(self):
        with HTTMock(failed_compilation_of_csdl):
            self.assertRaises(DataSiftApiException, self.client.compile, ("dummy csdl which is bad"))

    def test_is_valid_csdl_with_bad_data(self):
        with HTTMock(failed_compilation_of_csdl):
            self.assertFalse(self.client.is_valid("dummy csdl which is bad"))

    def test_is_valid_csdl_with_good_data(self):
        mock, expected = mock_output_of(self.client.validate)
        with HTTMock(mock):
            runs = 0
            for item in expected:
                runs+=1
                r = self.client.is_valid("dummy csdl which is valid")
                self.assertTrue(r)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_is_valid_csdl_cause_exception(self):
        with HTTMock(internal_server_error_with_json):
            self.assertRaises(DataSiftApiException, self.client.is_valid, ("csdl which turns into a teapot"))

    def test_error_handling_of_internal_server_errors(self):
        with HTTMock(internal_server_error):
            self.assertRaises(DataSiftApiFailure, self.client.balance)

    def test_error_handling_of_weird_errors(self):
        with HTTMock(weird_error):
            self.assertRaises(HTTPError, self.client.validate, ("csdl which turns into a teapot"))

    def test_client_usage(self):
        mock, expected = mock_output_of(self.client.usage)
        with HTTMock(mock):
            runs = 0
            for expected_output in expected:
                runs += 1
                results = self.client.usage()
                self.assertDictEqual(results.headers, {'content-type': 'application/json'})
                assert_dict_structure(self, results, expected_output)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_client_usage_with_parameter(self):
        mock, expected = mock_output_of(self.client.usage)
        with HTTMock(mock):
            runs = 0
            for expected_output in expected:
                runs += 1
                results = self.client.usage(period="day")
                assert_dict_structure(self, results, expected_output)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")


    def test_client_dpu(self):
        mock, expected = mock_output_of(self.client.dpu)
        with HTTMock(mock):
            runs = 0
            for expected_output in expected:
                runs += 1
                results = self.client.dpu("valid stream id")
                assert_dict_structure(self, results, expected_output)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    @unittest.skipIf(sys.version_info >= (3,0), "Mocking requests does not work correctly on py3")
    def test_client_pull(self):
        mock, expected = normal_pull_output()
        with HTTMock(mock):
            results = self.client.pull("dummy valid subscription id", size=2048, cursor=512)
            self.assertEquals(results.status_code, 200)
            self.assertEqual(len(results), len(expected), msg="get the same number of interactions out")
            self.assertEqual(len(results), len(results.raw), msg="number of messages mangled by conversion")
            self.assertDictEqual(results.headers, {})
            self.assertTrue(results.status_code == 200)
            for output, expected in zip(results, expected):
                assert_dict_structure(self, output, expected)

    def test_live_streaming_exceptions_warn_on_bad_starts(self):
        self.assertRaises(StreamSubscriberNotStarted, self.client.subscribe, ("hash"))
        self.client._stream_process_started = True
        func = self.client.subscribe("hash")
        self.assertRaises(DeleteRequired, func, ("hash"))

    def test_live_streaming_client_setup(self):
        mock, expected = mock_output_of(self.client.compile)

        with HTTMock(mock):
            @self.client.on_delete
            def on_delete(interaction):
                print( 'Deleted interaction %s ' % interaction)


            @self.client.on_open
            def on_open():
                print( 'Streaming ready, can start subscribing')
                csdl = 'interaction.content contains "music"'
                stream = self.client.compile(csdl)['hash']

                @self.client.subscribe(stream)
                def subscribe_to_hash(msg):
                    print(msg)


            @self.client.on_closed
            def on_close(wasClean, code, reason):
                print('Streaming connection closed')


            @self.client.on_ds_message
            def on_ds_message(msg):
                print('DS Message %s' % msg)

            self.client._stream_process_started = True
            self.client.start_stream_subscriber()

class TestMockedHistoricsClient(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.client = DataSiftClient(DataSiftConfig("testuser", "testapikey"))

    def test_can_prepare_historics_job(self):
        mock, expected = mock_output_of(self.client.historics.prepare)
        with HTTMock(mock):
            runs = 0
            for expected_output in expected:
                runs += 1
                results = self.client.historics.prepare("fake csdl hash", int(time.time()-60), int(time.time()), "my fake historics query", "twitter", sample=10)
                assert_dict_structure(self, results, expected_output)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_prepare_historics_job_with_real_data(self):
        with HTTMock(historics_prepare_live_example):
            results = self.client.historics.prepare("fake csdl hash", int(time.time()-60), int(time.time()), "my fake historics query", "twitter", sample=10)
            assert_dict_structure(self, results.raw, results)


    def test_preparing_historics_query_with_no_sources_throws_exception(self):
        self.assertRaises(HistoricSourcesRequired, self.client.historics.prepare, "fake csdl hash", int(time.time()-60), int(time.time()), "my fake historics query", [])

    def test_historics_successful_delete(self):
        with HTTMock(intentionally_blank):
            result = self.client.historics.delete("historics id of a thing we want to delete")
            self.assertEqual(result.status_code, 204)
            self.assertDictEqual(result, {})

    def test_can_start_a_historics_job(self):
        with HTTMock(intentionally_blank):
            result = self.client.historics.start("dummy historics ID")
            self.assertEqual(result.status_code, 204)
            self.assertDictEqual({}, result)


    def test_can_delete_a_historics_job(self):
        with HTTMock(intentionally_blank):
            result = self.client.historics.delete("dummy historics ID")
            self.assertEqual(result.status_code, 204)
            self.assertDictEqual({}, result)


    @unittest.skipIf(sys.version_info >= (3,0), "Mocking requests does not work correctly on py3")
    def test_can_get_historics_status(self):
        mock, expected_outputs = mock_output_of(self.client.historics.status, prep=json.dumps)
        with HTTMock(mock):
            runs = 0
            for expected_output in expected_outputs:
                runs += 1
                result = self.client.historics.status(int(time.time()-60), int(time.time()), sources=["twitter", "facebook"])
                self.assertListEqual(result, expected_output)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_rename_historics_query(self):
        with HTTMock(intentionally_blank):
            result = self.client.historics.update("dummy historics id", "new name")
            self.assertEqual(result.status_code, 204)
            self.assertDictEqual({}, result)


    def test_can_stop_a_historics_query(self):
        with HTTMock(intentionally_blank):
            result = self.client.historics.stop("dummy historics id", reason="because I need to test this")
            self.assertEqual(result.status_code, 204)
            self.assertDictEqual({}, result)

    def test_can_get_specific_historics_query(self):
        mock, expected_outputs = mock_output_of(self.client.historics.get_for)
        with HTTMock(mock):
            runs = 0
            for expected_output in expected_outputs:
                runs += 1
                result = self.client.historics.get_for("dummy historics id")
                self.assertEqual(result.status_code, 200)
                assert_dict_structure(self, result, expected_output)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_get__historics_queries(self):
        mock, expected_outputs = mock_output_of(self.client.historics.get)
        with HTTMock(mock):
            runs = 0
            for expected_output in expected_outputs:
                runs += 1
                result = self.client.historics.get(maximum=25, page=1)
                self.assertEqual(result.status_code, 200)
                assert_dict_structure(self, result, expected_output)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_get_historics_preview_to_throw_an_exception_with_no_sources(self):
        self.assertRaises(HistoricSourcesRequired, self.client.historics_preview.create, "stream hash", int(time.time()-60), [], [], int(time.time()))

    def test_can_create_a_historics_preview(self):
        with HTTMock(preview_create):
            results = self.client.historics_preview.create("stream hash", int(time.time()-60), [], "twitter", end=time.time())
            self.assertEqual(results.status_code, 202)

    def test_can_retrieve_a_historics_preview_job(self):
        mock, expected_outputs = mock_output_of(self.client.historics_preview.get)
        with HTTMock(mock):
            runs = 0
            for expected_output in expected_outputs:
                runs += 1
                result = self.client.historics_preview.get("preview id goes here")
                self.assertEqual(result.status_code, 200)
                assert_dict_structure(self, expected_output, result)
            self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

class TestMockedManagedSourcesClient(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.client = DataSiftClient(DataSiftConfig("testuser", "testapikey"))

    def test_can_create_managed_source(self):
        with HTTMock(source_create):
            result = self.client.managed_sources.create("facebook_page", "my facebook page test", [{"parameters":{"value":89021341890}}], [{"parameter":"value"}], parameters={"likes": True})
            self.assertEqual(result.status_code, 201)
            self.assertIn(u"status", result)

    def test_can_update_managed_source(self):
        with HTTMock(source_update):
            result = self.client.managed_sources.update("my managed source id", "facebook_page", "my managed source", [{"parameters":{"mysql_host": "foo"}}], [{"username":"whatever"}], parameters={"likes": False})
            self.assertEqual(result.status_code, 202)
            self.assertIn(u"status", result)

    def test_can_start_managed_source(self):
        mock, expected_outputs = mock_output_of(self.client.managed_sources.start)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.managed_sources.start("my managed source id")
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_stop_managed_source(self):
        mock, expected_outputs = mock_output_of(self.client.managed_sources.stop)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.managed_sources.stop("my managed source id")
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_delete_managed_source(self):
        with HTTMock(intentionally_blank):
            result = self.client.managed_sources.delete("my managed source id")
            self.assertEqual(result.status_code, 204)
            self.assertDictEqual({}, result)

    def test_can_retrieve_managed_sources_log(self):
        mock, expected_outputs = mock_output_of(self.client.managed_sources.log)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.managed_sources.log("my managed source", page=1, per_page=25)
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_get_managed_source(self):
       mock, expected_outputs = mock_output_of(self.client.managed_sources.get)
       runs = 0
       for expected_output in expected_outputs:
           runs += 1
           with HTTMock(mock):
               result = self.client.managed_sources.get(source_id="my managed source id", source_type="twitter", page=1, per_page=25)
           self.assertEqual(result.status_code, 200)
           assert_dict_structure(self, expected_output, result)
       self.assertNotEqual(runs, 0, "ensure that at least one case was tested")


class TestMockedPushClient(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.client = DataSiftClient(DataSiftConfig("testuser", "testapikey"))

    def test_can_validate_a_push_subscription(self):
        with HTTMock(intentionally_blank):
            result = self.client.push.validate("HTTP", {"delivery_frequency": 60, "url":"http://mywebsite:port/", "auth":{"type": "basic", "username": "myuserfordatasift", "password":"passwordfordatasiftuser"}})
            self.assertEqual(result.status_code, 204)
            self.assertDictEqual({}, result)

    def test_can_create_a_push_subscription_from_historics(self):
        mock, expected_outputs = mock_output_of(self.client.push.create_from_historics)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.push.create_from_historics("historics id", "my test push for historics", "pull", {})
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_create_a_push_subscription_from_hash(self):
        mock, expected_outputs = mock_output_of(self.client.push.create_from_hash)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.push.create_from_hash("my stream", "my test push for historics", "pull", {}, initial_status="paused", start=time.time()-60, end=time.time())
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_pause_a_push_subscription(self):
        mock, expected_outputs = mock_output_of(self.client.push.pause)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.push.pause("target subscription id")
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_resume_a_push_subscription(self):
        mock, expected_outputs = mock_output_of(self.client.push.resume)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.push.resume("target subscription id")
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_update_a_push_subscription(self):
        mock, expected_outputs = mock_output_of(self.client.push.update)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.push.update("target subscription id", {"foo": "bar"}, name="new name")
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_stop_a_push_subscription(self):
        mock, expected_outputs = mock_output_of(self.client.push.stop)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.push.stop("target subscription id")
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_delete_a_push_subscription(self):
         with HTTMock(intentionally_blank):
             result = self.client.push.delete("target subscription id")
             self.assertEqual(result.status_code, 204)
             self.assertDictEqual(result, {})

    def test_can_read_the_push_log(self):
        mock, expected_outputs = mock_output_of(self.client.push.log)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.push.log(subscription_id="target subscription id", page=1, per_page=25, order_by="request_time", order_dir="asc")
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_get_push_data_with_all_arguments(self):
        mock, expected_outputs = mock_output_of(self.client.push.get)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.push.get(subscription_id="target subscription id", stream="target hash", historics_id="target historics id", page=1, per_page=25, order_by="request_time", order_dir="desc", include_finished = True)
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")

    def test_can_get_push_data_with_no_arguments(self):
        mock, expected_outputs = mock_output_of(self.client.push.get)
        runs = 0
        for expected_output in expected_outputs:
            runs += 1
            with HTTMock(mock):
                result = self.client.push.get()
            self.assertEqual(result.status_code, 200)
            assert_dict_structure(self, expected_output, result)
        self.assertNotEqual(runs, 0, "ensure that at least one case was tested")





if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMockedClient)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMockedHistoricsClient)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMockedManagedSourcesClient)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMockedPushClient)
    unittest.TextTestRunner(verbosity=2).run(suite)
