import unittest, sys, os, json
from datetime import datetime
import testdata
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]
import datasift

class TestDefinition(unittest.TestCase):

    user = None
    mock_api_client = None

    def setUp(self):
        self.user = datasift.User(testdata.username, testdata.api_key)
        self.mock_api_client = datasift.mockapiclient.MockApiClient()
        self.user.set_api_client(self.mock_api_client)

    def test_construction(self):
        definition = datasift.Definition(self.user)
        self.assertEqual(definition.get(), '', 'Default definition CSDL is not empty')

    def test_construction_with_definition(self):
        definition = datasift.Definition(self.user, testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

    def test_construction_invalid_user(self):
        try:
            definition = datasift.Definition(testdata.username)
            self.fail('Expected InvalidDataError exception not thrown')
        except datasift.InvalidDataError:
            # Expected exception
            pass

    def test_construction_invalid_definition(self):
        try:
            definition = datasift.Definition(self.user, 1234)
            self.fail('Expected InvalidDataError exception not thrown')
        except datasift.InvalidDataError:
            # Expected exception
            pass

    def test_set_and_get(self):
        definition = datasift.Definition(self.user)
        self.assertEqual(definition.get(), '', 'Default definition CSDL is not empty')
        definition.set(testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

    def test_compile_success(self):
        response = {
            'response_code': 200,
            'data': {
                'hash':       testdata.definition_hash,
                'created_at': '2011-12-13 14:15:16',
                'dpu':        10,
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        definition = datasift.Definition(self.user, testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

        try:
            definition.compile()
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.CompileFailedError as e:
            self.fail('CompileFailedError: %s' % e)
        except datasift.APIError as (e, c):
            self.fail('APIError: %s' % e)

        self.assertEqual(self.user.get_rate_limit(), response['rate_limit'], 'Incorrect rate limit')
        self.assertEqual(self.user.get_rate_limit_remaining(), response['rate_limit_remaining'], 'Incorrect rate limit remaining')
        self.assertEqual(definition.get_hash(), response['data']['hash'], 'Incorrect hash')
        self.assertEqual(definition.get_created_at(), datetime.strptime(response['data']['created_at'], '%Y-%m-%d %H:%M:%S'), 'Incorrect created at date')
        self.assertEqual(definition.get_total_dpu(), response['data']['dpu'], 'Incorrect total DPU')

    def test_compile_failure(self):
        response = {
            'response_code': 400,
            'data': {
                'error': 'The target interactin.content does not exist',
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        definition = datasift.Definition(self.user, testdata.invalid_definition)
        self.assertEqual(definition.get(), testdata.invalid_definition, 'Definition CSDL not set correctly')

        try:
            definition.compile()
            self.fail('Expected CompileFailedError not thrown')
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.CompileFailedError as e:
            self.assertEqual(e.__str__(), response['data']['error'])
        except datasift.APIError as (e, c):
            self.fail('APIError: %s' % e)

    def test_compile_success_then_failure(self):
        response = {
            'response_code': 200,
            'data': {
                'hash':       testdata.definition_hash,
                'created_at': '2011-12-13 14:15:16',
                'dpu':        10,
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        definition = datasift.Definition(self.user, testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

        try:
            definition.compile()
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.CompileFailedError as e:
            self.fail('CompileFailedError: %s' % e)
        except datasift.APIError as (e, c):
            self.fail('APIError: %s' % e)

        self.assertEqual(self.user.get_rate_limit(), response['rate_limit'], 'Incorrect rate limit')
        self.assertEqual(self.user.get_rate_limit_remaining(), response['rate_limit_remaining'], 'Incorrect rate limit remaining')
        self.assertEqual(definition.get_hash(), response['data']['hash'], 'Incorrect hash')
        self.assertEqual(definition.get_created_at(), datetime.strptime(response['data']['created_at'], '%Y-%m-%d %H:%M:%S'), 'Incorrect created at date')
        self.assertEqual(definition.get_total_dpu(), response['data']['dpu'], 'Incorrect total DPU')

        definition.set(testdata.invalid_definition)
        self.assertEqual(definition.get(), testdata.invalid_definition, 'Definition CSDL not set correctly')

        response = {
            'response_code': 400,
            'data': {
                'error': 'The target interactin.content does not exist',
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        try:
            definition.compile()
            self.fail('Expected CompileFailedError not thrown')
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.CompileFailedError as e:
            self.assertEqual(e.__str__(), response['data']['error'])
        except datasift.APIError as (e, c):
            self.fail('APIError: %s' % e)

    def test_get_created_at(self):
        response = {
            'response_code': 200,
            'data': {
                'created_at': '2011-12-13 14:15:16',
                'dpu':        10,
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        definition = datasift.Definition(self.user, testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

        self.assertEqual(definition.get_created_at(), datetime.strptime(response['data']['created_at'], '%Y-%m-%d %H:%M:%S'), 'Incorrect created at date')

    def test_get_total_dpu(self):
        response = {
            'response_code': 200,
            'data': {
                'created_at': '2011-12-13 14:15:16',
                'dpu':        10,
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        definition = datasift.Definition(self.user, testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

        self.assertEqual(definition.get_total_dpu(), response['data']['dpu'], 'Incorrect total DPU')

    def test_get_dpu_breakdown(self):
        response = {
            'response_code': 200,
            'data': {
                'hash':       testdata.definition_hash,
                'created_at': '2011-12-13 14:15:16',
                'dpu':        4,
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        definition = datasift.Definition(self.user, testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

        self.assertEqual(definition.get_hash(), response['data']['hash'], 'Incorrect hash')

        response = {
            'response_code': 200,
            'data': {
                'detail': {
                    'contains': {
                        'count': 1,
                        'dpu':   4,
                        'targets': {
                            'interaction.content': {
                                'count': 1,
                                'dpu':   4,
                            },
                        },
                    },
                },
                'dpu': 4,
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        dpu = definition.get_dpu_breakdown()

        self.assertEqual(dpu, response['data'], 'The DPU breakdown is not as expected')
        self.assertEqual(definition.get_total_dpu(), response['data']['dpu'], 'The total DPU is incorrect')

    def test_get_dpu_breakdown_on_invalid_definition(self):
        definition = datasift.Definition(self.user, testdata.invalid_definition)
        self.assertEqual(definition.get(), testdata.invalid_definition, 'Definition CSDL not set correctly')

        response = {
            'response_code': 400,
            'data': {
                'error': 'The target interactin.content does not exist',
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        try:
            definition.get_dpu_breakdown()
            self.fail('Expected CompileFailedError not thrown')
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.CompileFailedError as e:
            self.assertEqual(e.__str__(), response['data']['error'])
        except datasift.APIError as (e, c):
            self.fail('APIError: %s' % e)

    def test_get_buffered(self):
        response = {
            'response_code': 200,
            'data': {
                'hash':       testdata.definition_hash,
                'created_at': '2011-12-13 14:15:16',
                'dpu':        4,
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        definition = datasift.Definition(self.user, testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

        self.assertEqual(definition.get_hash(), response['data']['hash'], 'Incorrect hash')

        response = {
            'response_code': 200,
            'data': {
                'stream': {
                    0: {
                        'interaction': {
                            'source': 'Snaptu',
                            'author': {
                                'username': 'nittolexia',
                                'name'    : 'nittosoetreznoe',
                                'id'      : 172192091,
                                'avatar'  : 'http://a0.twimg.com/profile_images/1429378181/gendowor_normal.jpg',
                                'link'    : 'http://twitter.com/nittolexia',
                            },
                            'type'      : 'twitter',
                            'link'      : 'http://twitter.com/nittolexia/statuses/89571192838684672',
                            'created_at': 'Sat, 09 Jul 2011 05:46:51 +0000',
                            'content'   : 'RT @ayyuchadel: Haha RT @nittolexia: Mending gak ush maen twitter dehh..RT @sansan_arie:',
                            'id'        : '1e0a9eedc207acc0e074ea8aecb2c5ea',
                        },
                        'twitter': {
                            'user': {
                                'name'           : 'nittosoetreznoe',
                                'description'    : 'fuck all',
                                'location'       : 'denpasar, bali',
                                'statuses_count' : 6830,
                                'followers_count': 88,
                                'friends_count'  : 111,
                                'screen_name'    : 'nittolexia',
                                'lang'           : 'en',
                                'time_zone'      : 'Alaska',
                                'id'             : 172192091,
                                'geo_enabled'    : True,
                            },
                            'mentions': {
                                0: 'ayyuchadel',
                                1: 'nittolexia',
                                2: 'sansan_arie',
                            },
                            'id'        : '89571192838684672',
                            'text'      : 'RT @ayyuchadel: Haha RT @nittolexia: Mending gak ush maen twitter dehh..RT @sansan_arie:',
                            'source'    : '<a href="http://www.snaptu.com" rel="nofollow">Snaptu</a>',
                            'created_at': 'Sat, 09 Jul 2011 05:46:51 +0000',
                        },
                        'klout': {
                            'score'        : 45,
                            'network'      : 55,
                            'amplification': 17,
                            'true_reach'   : 31,
                            'slope'        : 0,
                            'class'        : 'Networker',
                        },
                        'peerindex': {
                            'score': 30,
                        },
                        'language': {
                            'tag': 'da',
                        },
                    },
                },
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        interactions = definition.get_buffered()

        self.assertEqual(interactions, response['data']['stream'], 'Buffered interactions are not as expected')

    def test_get_consumer(self):
        response = {
            'response_code': 200,
            'data': {
                'hash':       testdata.definition_hash,
                'created_at': '2011-12-13 14:15:16',
                'dpu':        4,
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        definition = datasift.Definition(self.user, testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

        self.assertEqual(definition.get_hash(), response['data']['hash'], 'Incorrect hash')

        consumer = definition.get_consumer(datasift.StreamConsumerEventHandler())

if __name__ == '__main__':
    unittest.main()
