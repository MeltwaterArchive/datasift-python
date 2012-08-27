# encoding: utf-8

"""
The official DataSift API library for Python. This module provides access to
the REST API and also facilitates consuming streams.

Requires Python 2.4+.

Copyright (C) 2012 MediaSift Ltd. All Rights Reserved.

To use, 'import datasift' and create a datasift.User object passing in your
username and API key. See the examples folder for reference usage.
"""

import sys, os, urllib, urllib2, json, thread, threading, types
from datetime import datetime

__author__  = "Stuart Dallas <stuart@3ft9.com>"
__status__  = "beta"
__version__ = "0.5.0"
__date__    = "27 August 2012"

#-----------------------------------------------------------------------------
# Add this folder to the system path.
#-----------------------------------------------------------------------------
sys.path[0:0] = [os.path.dirname(__file__),]

#-----------------------------------------------------------------------------
# Module constants
#-----------------------------------------------------------------------------
USER_AGENT      = 'DataSiftPython/%s' % (__version__)
API_BASE_URL    = 'api.datasift.com/'
STREAM_BASE_URL = 'stream.datasift.com/'

#-----------------------------------------------------------------------------
# Check for SSL support.
#-----------------------------------------------------------------------------
try:
    import ssl
except ImportError:
    SSL_AVAILABLE = False
else:
    SSL_AVAILABLE = True

#-----------------------------------------------------------------------------
# Module exceptions.
#-----------------------------------------------------------------------------
class AccessDeniedError(Exception):
    """
    This exception is thrown when an access denied error is returned by the
    DataSift API.
    """
    pass

class APIError(Exception):
    """
    Thrown for errors that occur while talking to the DataSift API.
    """
    pass

class CompileFailedError(Exception):
    """
    Thrown when compilation of a definition fails.
    """
    pass

class InvalidDataError(Exception):
    """
    Thrown whenever invalid data is detected.
    """
    pass

class RateLimitExceededError(Exception):
    """
    Thrown when you exceed the API rate limit.
    """
    pass

class StreamError(Exception):
    """
    Thrown for errors to do with the streaming API.
    """
    pass

#-----------------------------------------------------------------------------
# Module-level utility functions.
#-----------------------------------------------------------------------------
def _exists(name):
    """
    Check whether the given name exists at the caller's local or global
    scope, or within the built-ins.
    """
    return (name in sys._getframe(1).f_locals  # caller's locals
         or name in sys._getframe(1).f_globals # caller's globals
         or name in vars(__builtin__)          # built-in
    )

#-----------------------------------------------------------------------------
# The User class - all interactions with the API should start here.
#-----------------------------------------------------------------------------
class User(object):
    """
    A User instance represents a DataSift user and provides access to all of
    the API functionality.
    """
    _username = False
    _api_key = False
    _rate_limit = -1
    _rate_limit_remaining = -1
    _api_client = None
    _use_ssl = SSL_AVAILABLE

    def __init__(self, username, api_key, use_ssl = True):
        """
        Initialise a User object with the given username and API key.
        """
        self._username = username
        self._api_key = api_key
        self._use_ssl = use_ssl

    def get_username(self):
        """
        Get the username.
        """
        return self._username

    def get_api_key(self):
        """
        Get the API key.
        """
        return self._api_key

    def use_ssl(self):
        """
        Returns true if stream connections should be using SSL.
        """
        if SSL_AVAILABLE:
            return self._use_ssl
        return False

    def enable_ssl(self, use_ssl):
        """
        Set whether stream connections should use SSL.
        """
        self._use_ssl = use_ssl

    def get_rate_limit(self):
        """
        Get the rate limit returned by the last API call, or -1 if no API calls
        have been made since this object was created.
        """
        return self._rate_limit

    def get_rate_limit_remaining(self):
        """
        Get the rate limit remaining as returned by the last API call, or -1 if
        no API calls have been made since this object was created.
        """
        return self._rate_limit_remaining

    def set_api_client(self, api_client):
        """
        Set the object to be used as the API client. This must be a subclass
        of the default API client class.
        """
        self._api_client = api_client

    def get_usage(self, period = 'hour'):
        """
        Get usage data for this user.
        """
        return self.call_api('usage', { 'period': period })

    def create_definition(self, csdl = ''):
        """
        Create a definition object for this user. If a CSDL parameter is
        provided then this will be used as the initial CSDL for the
        definition.
        """
        return Definition(self, csdl)

    def create_historic(self, hash, start, end, sources, sample, name):
        """
        Create a historic query based on this definition.
        """
        return Historic(self, hash, start, end, sources, sample, name)

    def get_historic(self, playback_id):
        """
        Get an existing Historics query from the API.
        """
        return Historic(self, playback_id)

    def list_historics(self, page = 1, per_page = 20):
        """
        Get the Historics queries in your account.
        """
        return Historic.list(self, page, per_page)

    def create_push_definition(self):
        """
        Create a new Push definition for this user.
        """
        return PushDefinition(self)

    def get_push_subscription(self, subscription_id):
        """
        Get a Push subscription from the API.
        """
        return PushSubscription.get(self, subscription_id)

    def get_push_subscription_log(self, subscription_id = False):
        """
        Get the logs for all Push subscriptions or the given subscription.
        """
        if subscription_id == False:
            return PushSubscription.get_logs(self)
        else:
            return self.get_push_subscription(subscription_id).get_log()

    def list_push_subscriptions(self, page = 1, per_page = 20, order_by = False, order_dir = False, include_finished = False, hash_type = False, hash = False):
        """
        Get the Push subscriptions in your account.
        """
        return PushSubscription.list(self, page, per_page, order_by, order_dir, include_finished, hash_type, hash)

    def get_consumer(self, hash, event_handler, consumer_type = 'http'):
        """
        Get a StreamConsumer object for the given hash via the given consumer
        type.
        """
        return StreamConsumer.factory(self, consumer_type, Definition(self, False, hash), event_handler)

    def get_multi_consumer(self, hashes, event_handler, consumer_type = 'http'):
        """
        Get a StreamConsumer object for the given set of hashes via the given
        consumer type.
        """
        return StreamConsumer.factory(self, consumer_type, hashes, event_handler)

    def get_useragent(self):
        """
        Get the useragent to be used for all API requests.
        """
        return USER_AGENT

    def call_api(self, endpoint, params):
        """
        Make a call to a DataSift API endpoint.
        """
        if self._api_client == None:
            self._api_client = ApiClient()
        res = self._api_client.call(self.get_username(), self.get_api_key(), endpoint, params, self.get_useragent())

        self._rate_limit = res['rate_limit']
        self._rate_limit_remaining = res['rate_limit_remaining']

        if res['response_code'] >= 200 and res['response_code'] <= 299:
            retval = res['data']
        elif res['response_code'] == 401:
            errmsg = 'Authentication failed'
            if 'data' in res and 'error' in res['data']:
                errmsg = res['data']['error']
            raise AccessDeniedError(errmsg)
        else:
            if res['response_code'] == 403:
                if self._rate_limit_remaining == 0:
                    raise RateLimitExceededError(res['data']['comment'])
            errmsg = 'Unknown error (%d)' % res['response_code']
            if 'data' in res and 'error' in res['data']:
                errmsg = res['data']['error']
            raise APIError(errmsg, res['response_code'])

        return retval

#-----------------------------------------------------------------------------
# The Definition class.
#-----------------------------------------------------------------------------
class Definition(object):
    """
    A Definition instance represents a stream definition.
    """
    _user = False
    _hash = False
    _created_at = False
    _total_dpu = False
    _csdl = ''

    def __init__(self, user, csdl = '', hash = False):
        """
        Initialise a Definition object, optionally priming it with the given CSDL and/or
        hash.
        """
        if not isinstance(user, User):
            raise InvalidDataError('Please supply a valid User object when creating a Definition object.')
        self._user = user
        self._hash = hash
        self.set(csdl)

    def get(self):
        """
        Get the definition's CSDL string.
        """
        if self._csdl == False:
            raise InvalidDataError('CSDL not available')
        return self._csdl

    def set(self, csdl):
        """
        Set the definition string.
        """
        if csdl == False:
            self._csdl = False
        else:
            if isinstance(csdl, unicode):
                csdl = csdl.encode('utf8')
            elif not isinstance(csdl, str):
                raise InvalidDataError('Definitions must be strings.')

            csdl = csdl.strip()

            # Reset the hash if the CSDL hash changed
            if self._csdl != csdl:
                self.clear_hash()

            self._csdl = csdl

    def get_hash(self):
        """
        Returns the hash for this definition. If the hash has not yet been
        obtained it compiles the definition first.
        """
        if self._hash == False:
            self.compile()
        return self._hash

    def clear_hash(self):
        """
        Reset the hash to false. The effect of this is to mark the definition
        as requiring compilation. Also resets other variables that depend on
        the CSDL.
        """
        if self._csdl == False:
            raise InvalidDataError('Cannot clear the hash of a hash-only definition object')
        self._hash = False
        self._created_at = False
        self._total_dpu = False

    def get_created_at(self):
        """
        Returns the date when the stream was first created. If the created at
        date has not yet been obtained it validates the definition first.
        """
        if self._csdl == False:
            raise InvalidDataError('Created at date not available')
        if self._created_at == False:
            try:
                self.validate()
            except InvalidDataError as e:
                pass
        return self._created_at

    def get_total_dpu(self):
        """
        Returns the total DPU of the stream. If the DPU has not yet been
        obtained it validates the definition first.
        """
        if self._csdl == False:
            raise InvalidDataError('Total DPU not available')
        if self._total_dpu == False:
            try:
                self.validate()
            except InvalidDataError as e:
                pass
        return self._total_dpu

    def compile(self):
        """
        Call the DataSift API to compile this definition. If compilation
        succeeds we store the details in the response.
        """
        if len(self._csdl) == 0:
            raise InvalidDataError('Cannot compile an empty definition')
        try:
            res = self._user.call_api('compile', { 'csdl': self._csdl })

            if not 'hash' in res:
                raise CompileFailedError('Compiled successfully but no hash in the response')
            self._hash = res['hash']

            if not 'created_at' in res:
                raise CompileFailedError('Compiled successfully but no created_at in the response')
            self._created_at = datetime.strptime(res['created_at'], '%Y-%m-%d %H:%M:%S')

            if not 'dpu' in res:
                raise CompileFailedError('Compiled successfully but no DPU in the response')
            self._total_dpu = res['dpu']
        except APIError as (msg, code):
            self.clear_hash()

            if code == 400:
                raise CompileFailedError(msg)
            else:
                raise CompileFailedError('Unexpected APIError code: %d [%s]' % (code, msg))

    def validate(self):
        """
        Call the DataSift API to validate this definition. If validation
        succeeds we store the details in the response.
        """
        if len(self._csdl) == 0:
            raise InvalidDataError('Cannot validate an empty definition')
        try:
            res = self._user.call_api('validate', { 'csdl': self._csdl })

            if not 'created_at' in res:
                raise CompileFailedError('Validated successfully but no created_at in the response')
            self._created_at = datetime.strptime(res['created_at'], '%Y-%m-%d %H:%M:%S')

            if not 'dpu' in res:
                raise CompileFailedError('Validated successfully but no DPU in the response')
            self._total_dpu = res['dpu']
        except APIError as (msg, code):
            self.clear_hash()

            if code == 400:
                raise CompileFailedError(msg)
            else:
                raise CompileFailedError('Unexpected APIError code: %d [%s]' % (code, msg))

    def get_dpu_breakdown(self):
        """
        Call the DataSift API to get the DPU breakdown for this definition.
        """
        if len(self._csdl) == 0:
            raise InvalidDataError('Cannot get the DPU breakdown for an empty definition')
        retval = self._user.call_api('dpu', { 'hash': self.get_hash() })
        if not 'dpu' in retval:
            raise APIError('No total DPU value present in the breakdown data', -1)
        self._total_dpu = retval['dpu']
        return retval

    def get_buffered(self, count = False, from_id = False):
        """
        Call the DataSift API to get buffered interactions.
        """
        if len(self._csdl) == 0:
            raise InvalidDataError('Cannot get buffered interactions for an empty definition')

        params = { 'hash': self.get_hash() }
        if count != False:
            params['count'] = count
        if from_id != False:
            params['interaction_id'] = from_id

        retval = self._user.call_api('stream', params)

        if not 'stream' in retval:
            raise APIError('No data in the response', -1)
        return retval['stream']

    def create_historic(self, start, end, sources, sample, name):
        """
        Create a historic query based on this definition.
        """
        return Historic(self._user, self.get_hash(), start, end, sources, sample, name)

    def get_consumer(self, event_handler, consumer_type = 'http'):
        """
        Returns a StreamConsumer-derived object for this definition for the
        given type.
        """
        if not isinstance(event_handler, StreamConsumerEventHandler):
            raise InvalidDataError('Please supply an object derived from StreamConsumerEventHandler when requesting a consumer')
        return StreamConsumer.factory(self._user, consumer_type, self, event_handler)

#-----------------------------------------------------------------------------
# The Historic class.
#-----------------------------------------------------------------------------
class Historic:
    """
    A Historic instance represents a historic query.
    """
    _user = None
    _playback_id = False
    _dpus = False
    _availability = {}
    _hash = False
    _start = False
    _end = False
    _created_at = False
    _sample = 100
    _sources = []
    _name = ''
    _status = 'created'
    _progress = 0
    _volume_info = {}
    _deleted = False

    @staticmethod
    def list(user, page = 1, per_page = 20):
        """
        Get a page of Historics queries in the given user's account, where
        each page contains up to per_page items.
        """
        if page < 1:
            raise InvalidDataError('The specified page number is invalid')
        if per_page < 1:
            raise InvalidDataError('The specified per_page value is invalid')

        params = {
            'page': page,
            'max': per_page,
        }

        res = user.call_api('historics/get', params)

        retval = {
            'count': res['count'],
            'historics': []
        }
        for historic in res['data']:
            retval['historics'].append(Historic(user, historic))

        return retval

    def __init__(self, user, hash, start = None, end = None, sources = None, sample = None, name = None):
        """
        Construct a new Historic query object from the supplied data. If the
        hash is a dict the object will be populated from that. If start is not
        supplied we'll attempt to load the object from the API using that as
        the playback ID. Otherwise a new Historics query is created using the
        data passed in.
        """
        if not isinstance(user, User):
            raise InvalidDataError('Please supply a valid User object when creating a Historic object.')
        self._user = user

        if isinstance(hash, dict):
            # Initialising from a dict
            self._init(hash)
        elif start == None:
            # The hash is the playback ID, get it from the API
            self._playback_id = hash
            self.reload_data()
        else:
            # Creating a new Historics query
            if isinstance(hash, Definition):
                hash = hash.get_hash()

            if start == 0:
                raise InvalidDataError('Please supply a valid start timestamp')
            if end == 0:
                raise InvalidDataError('Please supply a valid end timestamp')

            if not isinstance(sources, list) or len(sources) == 0:
                raise InvalidDataError('Please supply a valid array of sources')

            self._hash       = hash
            self._start      = start
            self._end        = end
            self._sources    = sources
            self._sample     = sample
            self._name       = name
            self._created_at = datetime.now()

    def _init(self, data):
        """
        Populate this object from the data in a dict.
        """
        if not 'id' in data:
            raise InvalidDataError('The playback ID is missing')
        self._playback_id = data['id']

        if not 'definition_id' in data:
            raise InvalidDataError('The stream hash is missing')
        self._hash = data['definition_id']

        if not 'name' in data:
            raise InvalidDataError('The name is missing')
        self._name = data['name']

        if not 'start' in data:
            raise InvalidDataError('The start timestamp is missing')
        self._start = data['start']

        if not 'end' in data:
            raise InvalidDataError('The end timestamp is missing')
        self._end = data['end']

        if not 'status' in data:
            raise InvalidDataError('The status is missing')
        self._status = data['status']

        if not 'progress' in data:
            raise InvalidDataError('The progress is missing')
        self._progress = data['progress']

        if not 'created_at' in data:
            raise InvalidDataError('The created at timestamp is missing')
        self._created_at = data['created_at']

        if not 'sources' in data:
            raise InvalidDataError('The sources is missing')
        self._sources = data['sources']

        if not 'sample' in data:
            raise InvalidDataError('The sample is missing')
        self._sample = data['sample']

        if not 'volume_info' in data:
            raise InvalidDataError('The volume info is missing')
        self._volume_info = data['volume_info']

        self._deleted = (self._status == 'deleted')

    def get_start_date(self):
        """
        Returns the start date for this query.
        """
        return self._start

    def get_end_date(self):
        """
        Returns the end date for this query.
        """
        return self._end

    def get_created_at(self):
        """
        Returns the created_at date for this query.
        """
        return self._created_at

    def get_name(self):
        """
        Returns the friendly name of this query.
        """
        return self._name

    def get_sources(self):
        """
        Returns the sources for this query.
        """
        return self._sources

    def get_progress(self):
        """
        Returns the progress percentage of this query.
        """
        return self._progress

    def get_sample(self):
        """
        Returns the sample percentage of this query.
        """
        return self._sample

    def get_status(self):
        """
        Returns the status of this query.
        """
        return self._status

    def get_volume_info(self):
        """
        Returns the volume_info for this query.
        """
        return self._volume_info

    def set_name(self, name):
        """
        Set the friendly name for this query.
        """
        if self._deleted:
            raise InvalidDataError('Cannot set the name of a deleted Historics query')

        if self._playback_id == False:
            # Not prepared yet, just set it locally
            self._name = name
        else:
            # Already sent to the API, update the name via that API
            try:
                res = self._user.call_api(
                    'historics/update',
                    {
                        'id': self._playback_id,
                        'name': self._name
                    })
                self.reload_data()
            except APIError as (e, c):
                if c == 400:
                    # Missing or invalid parameters
                    raise InvalidDataError(e)
                else:
                    raise APIError('Unexpected APIError code: %d [%s]' % (c, e))

    def get_hash(self):
        """
        Get the playback ID for this query. If the query has not yet been
        prepared this will be done automagically to get the hash.
        """
        if self._playback_id == False:
            self.prepare()
        return self._playback_id

    def get_stream_hash(self):
        """
        Get the hash for the stream this Historics query is using.
        """
        return self._hash

    def get_dpus(self):
        """
        Get the DPU cost. If the query has not yet been prepared this will be
        done automagically to obtain the cost.
        """
        if self._dpus == False:
            self.prepare()
        return self._dpus

    def get_availability(self):
        """
        Get the data availability info. If the query has not yet been prepared
        this will be done automagically to obtain the availability data.
        """
        if self._availability == False:
            self.prepare()
        return self._availability

    def reload_data(self):
        if self._deleted:
            raise InvalidDataError('Cannot set the name of a deleted Historics query')

        if self._playback_id == False:
            raise InvalidDataError('Cannot reload the data for a Historics query that hasn\'t been prepared')

        try:
            self._init(self._user.call_api(
                'historics/get',
                {
                    'id': self._playback_id
                }))

        except APIError as (e, c):
            if c == 400:
                # Missing or invalid parameters
                raise InvalidDataError(e)
            else:
                raise APIError('Unexpected APIError code: %d [%s]' % (c, e))

    def prepare(self):
        """
        Call the DataSift API to prepare this historic query.
        """
        if self._deleted:
            raise InvalidDataError('Cannot prepare a deleted Historics query')

        if self._playback_id != False:
            raise InvalidDataError('This historic query has already been prepared')

        try:
            res = self._user.call_api(
                'historics/prepare',
                {
                    'hash': self._hash,
                    'start': self._start,
                    'end': self._end,
                    'name': self._name,
                    'sources': ','.join(self._sources)
                })

            if not 'id' in res:
                raise APIError('Prepared successfully but no playback ID in the response', -1)
            self._playback_id = res['id']

            if not 'dpus' in res:
                raise APIError('Prepared successfully but no DPU cost in the response', -1)
            self._dpus = res['dpus']
        except APIError as (e, c):
            if c == 400:
                # Missing or invalid parameters
                raise InvalidDataError(e)
            else:
                raise APIError('Unexpected APIError code: %d [%s]' % (c, e))

    def start(self):
        """
        Start this historic query.
        """
        if self._deleted:
            raise InvalidDataError('Cannot start a deleted Historics query')

        if self._playback_id == False or len(self._playback_id) == 0:
            raise InvalidDataError('Cannot start a historic query that hasn\'t been prepared')

        try:
            res = self._user.call_api(
                    'historics/start',
                    {
                        'id': self._playback_id
                    })
        except APIError as (e, c):
            if c == 400:
                # Missing or invalid parameters
                raise InvalidDataError(e)
            elif c == 404:
                # Historic query not found
                raise InvalidDataError(e)
            else:
                raise APIError('Unexpected APIError code: %d [%s]' % (c, e))

    def stop(self):
        """
        Stop this historic query.
        """
        if self._deleted:
            raise InvalidDataError('Cannot stop a deleted Historics query')

        if self._playback_id == False or len(self._playback_id) == 0:
            raise InvalidDataError('Cannot stop a historic query that hasn\'t been prepared')

        try:
            res = self._user.call_api(
                    'historics/stop',
                    {
                        'id': self._playback_id
                    })
        except APIError as (e, c):
            if c == 400:
                # Missing or invalid parameters
                raise InvalidDataError(e)
            elif c == 404:
                # Historic query not found
                raise InvalidDataError(e)
            else:
                raise APIError('Unexpected APIError code: %d [%s]' % (c, e))

    def delete(self):
        """
        Delete this historic query.
        """
        if self._deleted:
            raise InvalidDataError('This Historics query has already been deleted')

        if self._playback_id == False or len(self._playback_id) == 0:
            raise InvalidDataError('Cannot delete a historic query that hasn\'t been prepared')

        try:
            res = self._user.call_api(
                    'historics/delete',
                    {
                        'id': self._playback_id
                    })
            self._deleted = True
        except APIError as (e, c):
            if c == 400:
                # Missing or invalid parameters
                raise InvalidDataError(e)
            elif c == 404:
                # Historic query not found
                raise InvalidDataError(e)
            else:
                raise APIError('Unexpected APIError code: %d [%s]' % (c, e))

#-----------------------------------------------------------------------------
# The PushDefinition class.
#-----------------------------------------------------------------------------
class PushDefinition:
    """
    A PushDefinition instance represents a push endpoint configuration.
    """
    OUTPUT_PARAMS_PREFIX = 'output_params.'
    _user = False
    _initial_status = ''
    _output_type = ''
    _output_params = {}

    def __init__(self, user):
        """
        Initialise a PushDefinition object.
        """
        if not isinstance(user, User):
            raise InvalidDataError('Please supply a valid User object when creating a PushDefinition object.')
        self._user = user

    def get_initial_status(self):
        """
        Get the initial status for subscriptions.
        """
        return self._initial_status

    def set_initial_status(self, status):
        """
        Set the initial status for subscriptions.
        """
        self._initial_status = status

    def get_output_type(self):
        """
        Get the output type.
        """
        return self._output_type

    def set_output_type(self, output_type):
        """
        Set the output type.
        """
        self._output_type = output_type

    def get_output_param(self, key):
        """
        Get an output parameter.
        """
        return self._output_params[key]

    def get_output_params(self):
        """
        Get all of the output parameters.
        """
        return self._output_params

    def set_output_param(self, key, val):
        """
        Set an output parameter.
        """
        self._output_params[key] = val

    def validate(self):
        """
        Validate the output type and parameters with the DataSift API.
        """
        params = { 'output_type': self.get_output_type() }
        for key in self._output_params:
            params[key] = self._output_params[key]

        retval = self._user.call_api('push/validate', params)

    def subscribe_definition(self, definition, name):
        """
        Subscribe this endpoint to a Definition.
        """
        return self.subscribe_stream_hash(definition.get_hash(), name)

    def subscribe_stream_hash(self, hash, name):
        """
        Subscribe this endpoint to a stream hash.
        """
        return self.subscribe('hash', hash, name)

    def subscribe_historic(self, historic, name):
        """
        Subscribe this endpoint to a Historic.
        """
        return self.subscribe_historic_playback_id(historic.get_hash(), name)

    def subscribe_historic_playback_id(self, playback_id, name):
        """
        Subscribe this endpoint to a historic playback ID.
        """
        return self.subscribe('playback_id', playback_id, name)

    def subscribe(self, hash_type, hash, name):
        """
        Subscribe this endpoint to a stream hash or historic playback ID. Note
        that this will activate the subscription if the initial status is set
        to active.
        """
        params = {
            'name': name,
            hash_type: hash,
            'output_type': self.get_output_type()
        }
        for key in self._output_params:
            params[self.OUTPUT_PARAMS_PREFIX + key] = self._output_params[key]
        if len(self.get_initial_status()) > 0:
            params['initial_status'] = self.get_initial_status()

        return PushSubscription(self._user, self._user.call_api('push/create', params))

#-----------------------------------------------------------------------------
# The PushSubscription class.
#-----------------------------------------------------------------------------
class PushSubscription(PushDefinition):
    """
    A PushSubscription instance represents the subscription of a push endpoint
    either a stream hash or a historic playback ID.
    """
    HASH_TYPE_STREAM   = 'stream';
    HASH_TYPE_HISTORIC = 'historic';

    STATUS_ACTIVE    = 'active';
    STATUS_PAUSED    = 'paused';
    STATUS_STOPPED   = 'stopped';
    STATUS_FINISHING = 'finishing';
    STATUS_FINISHED  = 'finished';
    STATUS_FAILED    = 'finished';
    STATUS_DELETED   = 'deleted';

    ORDERBY_ID           = 'id';
    ORDERBY_CREATED_AT   = 'created_at';
    ORDERBY_REQUEST_TIME = 'request_time';

    ORDERDIR_ASC  = 'asc';
    ORDERDIR_DESC = 'desc';

    _user         = False
    _id           = ''
    _created_at   = ''
    _name         = ''
    _status       = ''
    _hash         = ''
    _hash_type    = ''
    _last_request = None
    _last_success = None

    @staticmethod
    def get(user, id):
        """
        Get a push subscription by ID.
        """
        return PushSubscription(user, user.call_api('push/get', { 'id': id }))

    @staticmethod
    def list(user, page = 1, per_page = 20, order_by = False, order_dir = False, include_finished = False, hash_type = False, hash = False):
        """
        Get a page of push subscriptions in the given user's account, where
        each page contains up to per_page items. Results will be ordered
        according to the supplied ordering parameters.
        """
        if page < 1:
            raise InvalidDataError('The specified page number is invalid')
        if per_page < 1:
            raise InvalidDataError('The specified per_page value is invalid')
        if order_by == False:
            order_by = PushSubscription.ORDERBY_CREATED_AT
        if order_dir == False:
            order_dir = PushSubscription.ORDERDIR_ASC

        params = {
            'page': page,
            'per_page': per_page,
            'order_by': order_by,
            'order_dir': order_dir
        }

        if hash_type != False and hash != False:
            params[hash_type] = hash

        if include_finished == 1:
            params['include_finished'] = 1

        res = user.call_api('push/get', params)

        retval = {
            'count': res['count'],
            'subscriptions': []
        }
        for subscription in res['subscriptions']:
            retval['subscriptions'].append(PushSubscription(user, subscription))

        return retval

    @staticmethod
    def list_by_stream_hash(user, hash, page = 1, per_page = 20, order_by = False, order_dir = False):
        """
        Get a page of push subscriptions in the given user's account
        subscribed to the given stream hash, where each page contains up to
        per_page items. Results will be ordered according to the supplied
        ordering parameters.
        """
        return __class__.list(user, page, per_page, order_by, order_dir, False, 'hash', hash)

    @staticmethod
    def list_by_playback_id(user, playback_id, page = 1, per_page = 20, order_by = False, order_dir = False):
        """
        Get a page of push subscriptions in the given user's account
        subscribed to the given playback ID, where each page contains up to
        per_page items. Results will be ordered according to the supplied
        ordering parameters.
        """
        return __class__.list(user, page, per_page, order_by, order_dir, False, 'playback_id', playback_id)

    @staticmethod
    def get_logs(user, page = 1, per_page = 20, order_by = False, order_dir = False, id = False):
        """
        Page through recent push subscription log entries, specifying the sort
        order.
        """
        if page < 1:
            raise InvalidDataError('The specified page number is invalid')
        if per_page < 1:
            raise InvalidDataError('The specified per_page value is invalid')
        if order_by == False:
            order_by = PushSubscription.ORDERBY_REQUEST_TIME
        if order_dir == False:
            order_dir = PushSubscription.ORDERDIR_DESC

        params = {
            'page': page,
            'per_page': per_page,
            'order_by': order_by,
            'order_dir': order_dir
        }

        if id != False:
            params['id'] = id

        return user.call_api('push/log', params)

    def __init__(self, user, data):
        """
        Initialise a new object from data in a dict.
        """
        PushDefinition.__init__(self, user)
        self._init(data)

    def _init(self, data):
        """
        Populate this object from the data in a dict.
        """
        if not 'id' in data:
            raise InvalidDataError('No id found in subscription data')
        self._id = data['id']

        if not 'name' in data:
            raise InvalidDataError('No name found in subscription data')
        self._name = data['name']

        if not 'created_at' in data:
            raise InvalidDataError('No created_at found in subscription data')
        self._created_at = data['created_at']

        if not 'status' in data:
            raise InvalidDataError('No status found in subscription data')
        self._status = data['status']

        if not 'hash_type' in data:
            raise InvalidDataError('No hash_type found in subscription data')
        self._hash_type = data['hash_type']

        if not 'hash' in data:
            raise InvalidDataError('No hash found in subscription data')
        self._hash = data['hash']

        if not 'last_request' in data:
            raise InvalidDataError('No last_request found in subscription data')
        self._last_request = data['last_request']

        if not 'last_success' in data:
            raise InvalidDataError('No last_success found in subscription data')
        self._last_success = data['last_success']

        if not 'output_type' in data:
            raise InvalidDataError('No output_type found in subscription data')
        self._output_type = data['output_type']

        if not 'output_params' in data:
            raise InvalidDataError('No output_params found in subscription data')
        self._output_params = self._parse_output_params(data['output_params'])

    def _parse_output_params(self, params, prefix = ''):
        """
        Recursive method to parse the output_params as received from the API
        into the flattened, dot-notation used by the client libraries.
        """
        retval = {}
        for key in params:
            if isinstance(params[key], dict):
                res = self._parse_output_params(params[key], '%s%s.' % (prefix, key))
                for key in res:
                    retval[key] = res[key]
            else:
                retval['%s%s' % (prefix, key)] = params[key]
        return retval

    def reload(self):
        """
        Re-fetch this subscription from the API.
        """
        self._init(self._user.call_api('push/get', { 'id': self.get_id() }))

    def get_id(self):
        """
        Return the subscription ID.
        """
        return self._id;

    def get_name(self):
        """
        Return the subscription name.
        """
        return self._name

    def set_output_param(self, key, val):
        """
        Set an output parameter. Checks to see if the subscription has been
        deleted, and if not calls the base class to set the parameter.
        """
        if self.is_deleted():
            raise InvalidDataError('Cannot modify a deleted subscription')
        PushDefinition.set_output_param(self, key, val)

    def get_created_at(self):
        """
        Get the timestamp when this subscription was created.
        """
        return self._created_at

    def get_status(self):
        """
        Get the current status of this subscription. Make sure you call reload
        to get the latest data for this subscription first.
        """
        return self._status

    def is_deleted(self):
        """
        Returns True if this subscription has been deleted.
        """
        return self.get_status() == self.STATUS_DELETED

    def get_hash_type(self):
        """
        Get the hash type to which this subscription is subscribed.
        """
        return self._hash_type

    def get_hash(self):
        """
        Get the hash or playback ID to which this subscription is subscribed.
        """
        return self._hash

    def get_last_request(self):
        """
        Get the timestamp of the last push request.
        """
        return self._last_request

    def get_last_success(self):
        """
        Get the timestamp of the last successful push request.
        """
        return self._last_success

    def save(self):
        """
        Save changes to the name and output parameters of this subscription.
        """
        params = {
            'id': self.get_id(),
            'name': self.get_name()
        }

        for key in self.get_output_params():
            params['%s%s' % (self.OUTPUT_PARAMS_PREFIX, key)] = self.get_output_param(key)

        self._init(self._user.call_api('push/update', params))

    def pause(self):
        """
        Pause this subscription.
        """
        self._init(self._user.call_api('push/pause', { 'id': self.get_id() }))

    def resume(self):
        """
        Resume this subscription.
        """
        self._init(self._user.call_api('push/resume', { 'id': self.get_id() }))

    def stop(self):
        """
        Stop this subscription.
        """
        self._init(self._user.call_api('push/stop', { 'id': self.get_id() }))

    def delete(self):
        """
        Delete this subscription.
        """
        self._user.call_api('push/delete', { 'id': self.get_id() })
        # The delete API call doesn't return the object, so set the status
        # manually
        self._status = self.STATUS_DELETED

    def get_log(self, page = 1, per_page = 20, order_by = False, order_dir = False):
        """
        Get a page of the log for this subscription in the order specified.
        """
        return PushSubscription.get_logs(self._user, page, per_page, order_by, order_dir, self.get_id())

#-----------------------------------------------------------------------------
# The ApiClient class.
#-----------------------------------------------------------------------------
class ApiClient(object):
    """
    The default class used for accessing the DataSift API.
    """
    def call(self, username, api_key, endpoint, params = {}, user_agent = USER_AGENT):
        """
        Make a call to a DataSift API endpoint.
        """
        url = 'http://%s%s.json' % (API_BASE_URL, endpoint)
        headers = {
            'Auth': '%s:%s' % (username, api_key),
            'User-Agent': user_agent,
        }
        req = urllib2.Request(url, urllib.urlencode(params), headers)

        try:
            resp = urllib2.urlopen(req, None, 10)
        except urllib2.HTTPError as resp:
            pass
        except urllib2.URLError as err:
            raise APIError('Request failed: %s' % err, 503)

        # Handle a response with no data
        content = resp.read()
        if len(content) == 0:
            data = json.loads('{}')
        else:
            data = json.loads(content)
            if not data:
                raise APIError('Failed to decode the response', retval['response_code'])

        retval = {
            'response_code': resp.getcode(),
            'data': data,
            'rate_limit': resp.headers.getheader('x-ratelimit-limit'),
            'rate_limit_remaining': resp.headers.getheader('x-ratelimit-remaining'),
        }

        return retval

#-----------------------------------------------------------------------------
# The StreamConsumerEventHandler base class.
#-----------------------------------------------------------------------------
class StreamConsumerEventHandler(object):
    """
    A base class for implementing event handlers for StreamConsumers.
    """
    def on_connect(self, consumer):
        pass
    def on_interaction(self, consumer, interaction, hash):
        pass
    def on_deleted(self, consumer, interaction, hash):
        pass
    def on_warning(self, consumer, msg):
        pass
    def on_error(self, consumer, msg):
        pass
    def on_status(self, consumer, status, data):
        pass
    def on_disconnect(self, consumer):
        pass

#-----------------------------------------------------------------------------
# The StreamConsumer class. This class should never be used directly, but all
# protocol-specific StreamConsumers should inherit from it.
#-----------------------------------------------------------------------------
class StreamConsumer(object):
    """
    This is the base class for all protocol-specific StreamConsumer classes.
    """

    @staticmethod
    def factory(user, consumer_type, definition, event_handler):
        """
        Factory method for creating protocol-specific StreamConsumer objects.
        """
        try:
            consumer_module = __import__('streamconsumer_%s' % (consumer_type))
            return consumer_module.factory(user, definition, event_handler)
        except ImportError:
            raise InvalidDataError('Consumer type "%s" is unknown' % consumer_type)

    """
    Consumer type definitions.
    """
    TYPE_HTTP = 'http'

    """
    Possible states.
    """
    STATE_STOPPED = 0
    STATE_STARTING = 1
    STATE_RUNNING = 2
    STATE_STOPPING = 3

    """
    Class variables
    """
    _user = None
    _hashes = []
    _event_handler = None
    _state = 0
    _auto_reconnect = True

    def __init__(self, user, definition, event_handler):
        """
        Initialise a StreamConsumer object.
        """
        if not isinstance(user, User):
            raise InvalidDataError('Please supply a valid User object when creating a StreamConsumer object')
        self._user = user

        if isinstance(definition, types.StringTypes):
            self._hashes = self._user.create_definition(definition).get_hash()
        elif isinstance(definition, Definition):
            self._hashes = definition.get_hash()
        elif isinstance(definition, list):
            self._hashes = definition
        else:
            raise InvalidDataError('The definition must be a CSDL string, an array of hashes or a Definition object.')

        if len(self._hashes) == 0:
            raise InvalidDataError('No valid hashes found when creating the consumer.');

        self._event_handler = event_handler

    def consume(self, auto_reconnect = True):
        """
        Start consuming.
        """
        self._auto_reconnect = auto_reconnect
        self._state = self.STATE_STARTING
        self.on_start()

    def stop(self):
        """
        Stop the consumer.
        """
        if not self._is_running(True):
            raise InvalidDataError('Consumer state must be RUNNING before it can be stopped')
        self._state = self.STATE_STOPPING

    def _get_url(self):
        """
        Gets the URL for the required stream.
        """
        protocol = 'http'
        if self._user.use_ssl():
            protocol = 'https'
        if isinstance(self._hashes, list):
            return "%s://%smulti?hashes=%s" % (protocol, STREAM_BASE_URL, ','.join(self._hashes))
        else:
            return "%s://%s%s" % (protocol, STREAM_BASE_URL, self._hashes)

    def _get_auth_header(self):
        """
        Get the authorisation HTTP header.
        """
        return '%s:%s' % (self._user.get_username(), self._user.get_api_key())

    def _get_user_agent(self):
        """
        Get the user agent to send with the request.
        """
        return self._user.get_useragent()

    def _is_running(self, allow_starting = False):
        """
        Is the consumer running?
        """
        return (allow_starting and self._state == self.STATE_STARTING) or self._state == self.STATE_RUNNING

    def _get_state(self):
        """
        Get the consumer state.
        """
        return self._state

    def _on_connect(self):
        """
        Called when the stream socket has connected.
        """
        self._state = self.STATE_RUNNING
        self._event_handler.on_connect(self)

    def _on_data(self, json_data):
        """
        Called for each complete chunk of JSON data is received.
        """
        try:
            data = json.loads(json_data)
        except:
            if self._is_running():
                self._on_error('Failed to decode JSON: %s' % json_data)
        else:
            if 'status' in data:
                # Status notification
                if data['status'] == 'failure' or data['status'] == 'error':
                    self._on_error(data['message'])
                    self.stop()
                elif data['status'] == 'warning':
                    self._on_warning(data['message'])
                else:
                    status = data['status']
                    del data['status']
                    self._on_status(status, data)
            elif 'hash' in data:
                # Muli-stream data
                if 'deleted' in data['data'] and data['data']['deleted']:
                    self._event_handler.on_deleted(self, data['data'], data['hash'])
                else:
                    self._event_handler.on_interaction(self, data['data'], data['hash'])
            elif 'interaction' in data:
                # Single stream data
                if 'deleted' in data and data['deleted']:
                    self._event_handler.on_deleted(self, data, self._hashes)
                else:
                    self._event_handler.on_interaction(self, data, self._hashes)
            else:
                # Unknown message
                self._on_error('Unhandled data received: %s' % (json_data))

    def _on_error(self, message):
        """
        Called when an error occurs. Errors are considered unrecoverable so
        we stop the consumer.
        """
        # Stop the consumer if we get an error
        if self._is_running():
            self.stop()
        self._event_handler.on_error(self, message)

    def _on_warning(self, message):
        """
        Called when a warning is raised or received.
        """
        self._event_handler.on_warning(self, message)

    def _on_status(self, status, data):
        """
        Called when a status message is raised or received.
        """
        self._event_handler.on_status(self, status, data)

    def _on_disconnect(self):
        """
        Called when the stream socket is disconnected.
        """
        self._event_handler.on_disconnect(self)
