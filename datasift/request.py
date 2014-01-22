"""
Thin wrapper around the requests library.
"""

import json
import requests

from datasift import USER_AGENT
from datasift.exceptions import DataSiftApiException


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
        return Response(self('get', path, params=params, headers=headers))

    def post(self, path, params=None, headers=None, data=None):
        return Response(self('post', path, params=params, headers=headers, data=data))

    def json(self, path, data):
        """Convenience method for posting JSON content."""
        data = data if isinstance(data, basestring) else json.dumps(data)
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

    ## Helpers

    def path(self, *args):
        return '/'.join(a.strip('/') for a in args if a)

    def dicts(self, *dicts):
        return dict(kv for d in dicts if d for kv in d.iteritems())


class DatasiftAuth(object):

    def __init__(self, user, key):
        assert user, "Invalid user '%s'" % user
        assert key, "Invalid key '%s'" % key
        self.user, self.key = user, key

    def __call__(self, request):
        request.headers['Authorization'] = '%s:%s' % (self.user, self.key)
        return request

class Response(dict):
    """ Wrapper for a response from the DataSift REST API, can be accessed as a dict to access returned data.

        :param response: HTTP response to wrap
        :type response: requests.response
        :param parser: optional parser to overload how the data is loaded
        :type parser: func
        :raises: DataSiftApiException, requests.exceptions.HTTPError
    """
    def __init__(self, response, parser=json.loads):
        self._response = response
        self._parser = parser
        self.data = None
        # Parse returned data and raise any exceptions
        if self.status_code != 204:
            self.data = self._parser(self._response.text)
            self.update(self.data)
            if "error" in self.data:
                raise DataSiftApiException(self)
        self._response.raise_for_status()


    @property
    def status_code(self):
        """HTTP Status Code of the Response"""
        return self._response.status_code

    @property
    def headers(self):
        """HTTP Headers of the Response"""
        return dict(self._response.headers)

    def str(self):
        if self.status_code < 400:
            return '%d %s' % (self.status_code, self.data)
        return str(self.status_code)
