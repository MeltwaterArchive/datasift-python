"""
Thin wrapper around the requests library.
"""

import json as jsonlib
import requests
import six

from datasift import USER_AGENT
from datasift.exceptions import DataSiftApiException, DataSiftApiFailure, AuthException


class PartialRequest(object):

    API_SCHEME = 'https'
    API_HOST = 'api.datasift.com'
    API_VERSION = 'v1.1'
    HEADERS = (
        ('User-Agent', USER_AGENT),
    )

    def __init__(self, auth, prefix=None, headers=None, timeout=None, proxies=None, verify=True):
        self.auth = auth
        self.prefix = prefix
        self.headers = headers
        self.timeout = timeout
        self.proxies = proxies
        self.verify = verify

    def get(self, path, params=None, headers=None):
        return self.build_response(self('get', path, params=params, headers=headers))

    def post(self, path, params=None, headers=None, data=None):
        return self.build_response(self('post', path, params=params, headers=headers, data=data))

    def json(self, path, data):
        """Convenience method for posting JSON content."""
        data = data if isinstance(data, six.string_types) else jsonlib.dumps(data)
        return self.post(path, headers={'Content-Type': 'application/json'}, data=data)

    def __call__(self, method, path, params=None, data=None, headers=None):
        url = u'%s://%s' % (self.API_SCHEME, self.path(self.API_HOST, self.API_VERSION, self.prefix, path))
        return requests.request(method, url,
                                params=params, data=data, auth=self.auth,
                                headers=self.dicts(self.headers, headers, dict(self.HEADERS)),
                                timeout=self.timeout,
                                proxies=self.proxies,
                                verify=self.verify)

    ## Builders

    def with_headers(self, headers):
        return PartialRequest(self.auth, prefix=self.prefix,
                              headers=self.dicts(self.headers, dict(headers)),
                              timeout=self.timeout, proxies=self.proxies, verify=self.verify)

    def with_prefix(self, path, *args):
        prefix = '/'.join((path,) + args)
        return PartialRequest(self.auth, prefix, self.headers, self.timeout, self.proxies, self.verify)


    def build_response(self, response, parser=jsonlib.loads):
        """ Builds a List or Dict response object.

            Wrapper for a response from the DataSift REST API, can be accessed as a list.

            :param response: HTTP response to wrap
            :type response: requests.response
            :param parser: optional parser to overload how the data is loaded
            :type parser: func
            :raises: DataSiftApiException, DataSiftApiFailure, AuthException, requests.exceptions.HTTPError
        """
        if response.status_code != 204:
            try:
                data = parser(response.text)
            except ValueError as e:
                raise DataSiftApiFailure("Unable to decode returned data.")
            if "error" in data:
                if response.status_code == 401:
                    raise AuthException(data)
                raise DataSiftApiException(Response(response, data))
            response.raise_for_status()
            if isinstance(data, dict):
                return Response(response, data)
            elif isinstance(data, (list, map)):
                return ListResponse(response, data)

        else:
            # empty dict
            return Response(response, {})

    ## Helpers

    def path(self, *args):
        return '/'.join(a.strip('/') for a in args if a)

    def dicts(self, *dicts):
        return dict(kv for d in dicts if d for kv in d.items())


class DatasiftAuth(object):

    def __init__(self, user, key):
        assert user, "Invalid user '%s'" % user
        assert key, "Invalid key '%s'" % key
        self.user, self.key = user, key

    def __call__(self, request):
        request.headers['Authorization'] = '%s:%s' % (self.user, self.key)
        return request

class ListResponse(list):
    """ Wrapper for a response from the DataSift REST API, can be accessed as a list.

        :param response: HTTP response to wrap
        :type response: requests.response
        :param data: data to wrap
        :type data: list
        :raises: DataSiftApiException, DataSiftApiFailure, AuthException, requests.exceptions.HTTPError
    """
    def __init__(self, response, data):
        self._response = response
        self.extend(data)

    @property
    def status_code(self):
        """HTTP Status Code of the Response"""
        return self._response.status_code

    @property
    def headers(self):
        """HTTP Headers of the Response"""
        return dict(self._response.headers)

class Response(dict):
    """ Wrapper for a response from the DataSift REST API, can be accessed as a dict.

        :param response: HTTP response to wrap
        :type response: requests.response
        :param parser: optional parser to overload how the data is loaded
        :type parser: func
        :raises: DataSiftApiException, DataSiftApiFailure, AuthException, requests.exceptions.HTTPError
    """
    def __init__(self, response, data):
        self._response = response
        self.update(data)

    @property
    def status_code(self):
        """HTTP Status Code of the Response"""
        return self._response.status_code

    @property
    def headers(self):
        """HTTP Headers of the Response"""
        return dict(self._response.headers)


