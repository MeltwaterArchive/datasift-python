import unittest, sys, os, json
from datetime import datetime
import testdata
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]
import datasift

class TestPush(unittest.TestCase):

    user = None
    mock_api_client = None

    def setUp(self):
        self.user = datasift.User(testdata.username, testdata.api_key)
        self.mock_api_client = datasift.mockapiclient.MockApiClient()
        self.user.set_api_client(self.mock_api_client)
        self.pushdef = datasift.PushDefinition(self.user)

    def test_construction(self):
        self.assertEqual(self.pushdef.get_initial_status(), '', 'Default initial status is not empty')
        self.assertEqual(self.pushdef.get_output_type(), '', 'Default output type is not empty')
        self.assertEqual(self.pushdef.get_output_params(), {}, 'Default output params is not empty')
        self.assertEqual(self.pushdef.OUTPUT_PARAMS_PREFIX, 'output_params.', 'Output param prefix is incorrect')

    def test_initial_status(self):
        self.assertEqual(self.pushdef.get_initial_status(), '', 'Default initial status is not empty')
        self.pushdef.set_initial_status(testdata.push_status)
        self.assertEqual(self.pushdef.get_initial_status(), datasift.PushSubscription.STATUS_ACTIVE, 'Initial status not set to the new value')

    def test_output_type(self):
        self.assertEqual(self.pushdef.get_output_type(), '', 'Default initial status is not empty')
        self.pushdef.set_output_type('http')
        self.assertEqual(self.pushdef.get_output_type(), 'http', 'Output type not set to the new value')

    def test_output_params(self):
        self.assertEqual(self.pushdef.get_output_params(), {}, 'Default output params is not empty')
        for key in testdata.push_output_params:
            self.pushdef.set_output_param(key, testdata.push_output_params[key])
        for key in testdata.push_output_params:
            self.assertEqual(self.pushdef.get_output_param(key), testdata.push_output_params[key], 'Output param %s is incorrect' % key)

    def test_validate_success(self):
        self._populate_pushdef()

        response = {
            'response_code': 204,
            'data': {},
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        try:
            self.pushdef.validate()
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.APIError as e:
            self.fail('APIError: %s' % e)

    def test_validate_failed(self):
        self._populate_pushdef(True)

        response = {
            'response_code': 400,
            'data': {
                'error': 'Bad request,The delivery frequency is required'
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        try:
            self.pushdef.validate()
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.APIError as (e, c):
            if c == 400:
                self.assertEqual(e, response['data']['error'], 'The failure error is incorrect')
            else:
                self.fail('APIError: [%d] %s' % (c, e))

    def test_subscribe_definition(self):
        definition = datasift.Definition(self.user, testdata.definition)
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
        self.assertEqual(definition.get_hash(), testdata.definition_hash, 'Definition hash not set correctly')

        self._populate_pushdef()

        response = {
            'response_code': 200,
            'data': {
                'id': testdata.push_id,
                'name': testdata.push_name,
                'created_at': testdata.push_created_at,
                'status': testdata.push_status,
                'hash': testdata.push_hash,
                'hash_type': testdata.push_hash_stream_type,
                'output_type': testdata.push_output_type,
                'output_params': {
                    'delivery_frequency': testdata.push_output_params['delivery_frequency'],
                    'url': testdata.push_output_params['url'],
                    'auth': {
                        'type': testdata.push_output_params['auth.type'],
                        'username': testdata.push_output_params['auth.username'],
                        'password': testdata.push_output_params['auth.password'],
                    },
                },
                'last_request': None,
                'last_success': None
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        pushsub = self.pushdef.subscribe_definition(definition, testdata.push_name)

        self.assertEqual(pushsub.get_id(), testdata.push_id, 'The subscription ID is incorrect')
        self.assertEqual(pushsub.get_name(), testdata.push_name, 'The subscription name is incorrect')
        self.assertEqual(pushsub.get_created_at(), testdata.push_created_at, 'The subscription created_at is incorrect')
        self.assertEqual(pushsub.get_status(), testdata.push_status, 'The subscription status is incorrect')
        self.assertEqual(pushsub.get_output_type(), testdata.push_output_type, 'The subscription output_type is incorrect')
        self.assertEqual(pushsub.get_hash_type(), testdata.push_hash_stream_type, 'The subscription hash_type is incorrect')
        self.assertEqual(pushsub.get_hash(), testdata.push_hash, 'The subscription hash is incorrect')
        self.assertEqual(pushsub.get_output_param('delivery_frequency'), testdata.push_output_params['delivery_frequency'], 'The subscription delivery_frequency is incorrect')
        self.assertEqual(pushsub.get_output_param('url'), testdata.push_output_params['url'], 'The subscription url is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.type'), testdata.push_output_params['auth.type'], 'The subscription auth.type is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.username'), testdata.push_output_params['auth.username'], 'The subscription auth.username is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.password'), testdata.push_output_params['auth.password'], 'The subscription auth.password is incorrect')

    def test_subscribe_stream_hash(self):
        self._populate_pushdef()

        response = {
            'response_code': 200,
            'data': {
                'id': testdata.push_id,
                'name': testdata.push_name,
                'created_at': testdata.push_created_at,
                'status': testdata.push_status,
                'hash': testdata.push_hash,
                'hash_type': testdata.push_hash_stream_type,
                'output_type': testdata.push_output_type,
                'output_params': {
                    'delivery_frequency': testdata.push_output_params['delivery_frequency'],
                    'url': testdata.push_output_params['url'],
                    'auth': {
                        'type': testdata.push_output_params['auth.type'],
                        'username': testdata.push_output_params['auth.username'],
                        'password': testdata.push_output_params['auth.password'],
                    },
                },
                'last_request': None,
                'last_success': None
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        pushsub = self.pushdef.subscribe_stream_hash(testdata.push_hash, testdata.push_name)

        self.assertEqual(pushsub.get_id(), testdata.push_id, 'The subscription ID is incorrect')
        self.assertEqual(pushsub.get_name(), testdata.push_name, 'The subscription name is incorrect')
        self.assertEqual(pushsub.get_created_at(), testdata.push_created_at, 'The subscription created_at is incorrect')
        self.assertEqual(pushsub.get_status(), testdata.push_status, 'The subscription status is incorrect')
        self.assertEqual(pushsub.get_output_type(), testdata.push_output_type, 'The subscription output_type is incorrect')
        self.assertEqual(pushsub.get_hash_type(), testdata.push_hash_stream_type, 'The subscription hash_type is incorrect')
        self.assertEqual(pushsub.get_hash(), testdata.push_hash, 'The subscription hash is incorrect')
        self.assertEqual(pushsub.get_output_param('delivery_frequency'), testdata.push_output_params['delivery_frequency'], 'The subscription delivery_frequency is incorrect')
        self.assertEqual(pushsub.get_output_param('url'), testdata.push_output_params['url'], 'The subscription url is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.type'), testdata.push_output_params['auth.type'], 'The subscription auth.type is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.username'), testdata.push_output_params['auth.username'], 'The subscription auth.username is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.password'), testdata.push_output_params['auth.password'], 'The subscription auth.password is incorrect')

    def test_subscribe_historic(self):
        definition = datasift.Definition(self.user, testdata.definition)
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
        self.assertEqual(definition.get_hash(), testdata.definition_hash, 'Definition hash not set correctly')

        response = {
            'response_code': 200,
            'data': {
                'dpus': testdata.historic_dpus,
                'id': testdata.historic_id,
                'availability': {
                    'start': 12345678,
                    'end': 124356376,
                    'sources': {
                        'twitter': {
                            'status': '99%',
                            'versions': [3],
                            'augmentations': {
                                'klout': '50%',
                                'links': '100%' 
                            }
                        },
                        'facebook': {
                            'status': '99%',
                            'versions': [2,3],
                            'augmentations': {
                                'links': '95%' 
                            }
                        }
                    }
                }
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        historic = definition.create_historic(testdata.historic_start_date, testdata.historic_end_date, testdata.historic_sources, testdata.historic_sample, testdata.historic_name)
        self.assertEqual(historic.get_hash(), testdata.historic_id, 'The historic playback ID is incorrect')

        self._populate_pushdef()

        response = {
            'response_code': 200,
            'data': {
                'id': testdata.push_id,
                'name': testdata.push_name,
                'created_at': testdata.push_created_at,
                'status': testdata.push_status,
                'hash': testdata.historic_id,
                'hash_type': testdata.push_hash_historic_type,
                'output_type': testdata.push_output_type,
                'output_params': {
                    'delivery_frequency': testdata.push_output_params['delivery_frequency'],
                    'url': testdata.push_output_params['url'],
                    'auth': {
                        'type': testdata.push_output_params['auth.type'],
                        'username': testdata.push_output_params['auth.username'],
                        'password': testdata.push_output_params['auth.password'],
                    },
                },
                'last_request': None,
                'last_success': None
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        pushsub = self.pushdef.subscribe_definition(definition, testdata.push_name)

        self.assertEqual(pushsub.get_id(), testdata.push_id, 'The subscription ID is incorrect')
        self.assertEqual(pushsub.get_name(), testdata.push_name, 'The subscription name is incorrect')
        self.assertEqual(pushsub.get_created_at(), testdata.push_created_at, 'The subscription created_at is incorrect')
        self.assertEqual(pushsub.get_status(), testdata.push_status, 'The subscription status is incorrect')
        self.assertEqual(pushsub.get_output_type(), testdata.push_output_type, 'The subscription output_type is incorrect')
        self.assertEqual(pushsub.get_hash_type(), testdata.push_hash_historic_type, 'The subscription hash_type is incorrect')
        self.assertEqual(pushsub.get_hash(), testdata.historic_id, 'The subscription hash is incorrect')
        self.assertEqual(pushsub.get_output_param('delivery_frequency'), testdata.push_output_params['delivery_frequency'], 'The subscription delivery_frequency is incorrect')
        self.assertEqual(pushsub.get_output_param('url'), testdata.push_output_params['url'], 'The subscription url is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.type'), testdata.push_output_params['auth.type'], 'The subscription auth.type is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.username'), testdata.push_output_params['auth.username'], 'The subscription auth.username is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.password'), testdata.push_output_params['auth.password'], 'The subscription auth.password is incorrect')

    def test_subscribe_historic_playback_id(self):
        self._populate_pushdef()

        response = {
            'response_code': 200,
            'data': {
                'id': testdata.push_id,
                'name': testdata.push_name,
                'created_at': testdata.push_created_at,
                'status': testdata.push_status,
                'hash': testdata.push_hash,
                'hash_type': testdata.push_hash_historic_type,
                'output_type': testdata.push_output_type,
                'output_params': {
                    'delivery_frequency': testdata.push_output_params['delivery_frequency'],
                    'url': testdata.push_output_params['url'],
                    'auth': {
                        'type': testdata.push_output_params['auth.type'],
                        'username': testdata.push_output_params['auth.username'],
                        'password': testdata.push_output_params['auth.password'],
                    },
                },
                'last_request': None,
                'last_success': None
            },
            'rate_limit':           200,
            'rate_limit_remaining': 150,
        }
        self.mock_api_client.set_response(response)

        pushsub = self.pushdef.subscribe_stream_hash(testdata.push_hash, testdata.push_name)

        self.assertEqual(pushsub.get_id(), testdata.push_id, 'The subscription ID is incorrect')
        self.assertEqual(pushsub.get_name(), testdata.push_name, 'The subscription name is incorrect')
        self.assertEqual(pushsub.get_created_at(), testdata.push_created_at, 'The subscription created_at is incorrect')
        self.assertEqual(pushsub.get_status(), testdata.push_status, 'The subscription status is incorrect')
        self.assertEqual(pushsub.get_output_type(), testdata.push_output_type, 'The subscription output_type is incorrect')
        self.assertEqual(pushsub.get_hash_type(), testdata.push_hash_historic_type, 'The subscription hash_type is incorrect')
        self.assertEqual(pushsub.get_hash(), testdata.push_hash, 'The subscription hash is incorrect')
        self.assertEqual(pushsub.get_output_param('delivery_frequency'), testdata.push_output_params['delivery_frequency'], 'The subscription delivery_frequency is incorrect')
        self.assertEqual(pushsub.get_output_param('url'), testdata.push_output_params['url'], 'The subscription url is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.type'), testdata.push_output_params['auth.type'], 'The subscription auth.type is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.username'), testdata.push_output_params['auth.username'], 'The subscription auth.username is incorrect')
        self.assertEqual(pushsub.get_output_param('auth.password'), testdata.push_output_params['auth.password'], 'The subscription auth.password is incorrect')

    def _populate_pushdef(self, with_invalid_output_params = False):
        self.pushdef.set_output_type(testdata.push_output_type)
        for key in testdata.push_output_params:
            if not with_invalid_output_params or key != 'delivery_frequency':
                self.pushdef.set_output_param(key, testdata.push_output_params[key])

if __name__ == '__main__':
    unittest.main()
