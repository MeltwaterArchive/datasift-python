
"""
Thin wrapper around the requests library.
"""

import json
import requests

from datasift import USER_AGENT


class PartialRequest(object):

    API_SCHEME  = 'https'
    API_HOST    = 'api.datasift.com'
    API_VERSION = 'v1.1'
    HEADERS     = (
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
        return  '/'.join(a.strip('/') for a in args if a)

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


class Response(object):
    def __init__(self, response, parser=json.loads):
        self._response = response
        self._parser = parser
        self._parsed = False
        self._data = None

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def headers(self):
        return dict(self._response.headers)

    @property
    def data(self):
        """Get data or raise an exception"""
        if not self._parsed:
            self._parsed = True
            # TODO: Wrap exceptions(?)
            self._response.raise_for_status
            if self.status_code != 204:
                self._data = self._parser(self._response.text)
        return self._data

