"""
Thin wrapper around the requests library.
"""

import json as jsonlib
import requests
import six

from datasift import USER_AGENT
from datasift.output_mapper import outputmapper
from datasift.exceptions import DataSiftApiException, DataSiftApiFailure, AuthException, RateLimitException
from datasift.requests_ssl import SslHttpAdapter


def json_decode_wrapper(headers, data):
    return jsonlib.loads(data)


class PartialRequest(object):
    """ Internal class used to represent a yet-to-be-completed request """

    API_SCHEME = 'https'
    API_HOST = 'api.datasift.com'
    API_VERSION = 'v1.1'
    HEADERS = (
        ('User-Agent', USER_AGENT % API_VERSION),
    )

    def __init__(self, auth, prefix=None, ssl=True, headers=None, timeout=None, proxies=None, verify=True):
        self.auth = auth
        if not ssl:
            self.API_SCHEME = "http"
        self.prefix = prefix
        self.headers = headers
        self.timeout = timeout
        self.proxies = proxies
        self.verify = verify
        self.session = requests.Session()
        self.adapter = SslHttpAdapter()
        self.session.mount("https://", self.adapter)

    def get(self, path, params=None, headers=None):
        return self.build_response(self('get', path, params=params, headers=headers), path=path)

    def post(self, path, params=None, headers=None, data=None):
        return self.build_response(self('post', path, params=params, headers=headers, data=data), path=path)

    def json(self, path, data):
        """Convenience method for posting JSON content."""
        data = data if isinstance(data, six.string_types) else jsonlib.dumps(data)
        return self.post(path, headers={'Content-Type': 'application/json'}, data=data)

    def __call__(self, method, path, params=None, data=None, headers=None):
        url = u'%s://%s' % (self.API_SCHEME, self.path(self.API_HOST, self.API_VERSION, self.prefix, path))
        return self.session.request(method, url,
                                    params=params, data=data, auth=self.auth,
                                    headers=self.dicts(self.headers, headers, dict(self.HEADERS)),
                                    timeout=self.timeout,
                                    proxies=self.proxies,
                                    verify=self.verify)

    # Builders

    def with_prefix(self, path, *args):
        prefix = '/'.join((path,) + args)
        return PartialRequest(self.auth, prefix, self.headers, self.timeout, self.proxies, self.verify)

    def build_response(self, response, path=None, parser=json_decode_wrapper):
        """ Builds a List or Dict response object.

            Wrapper for a response from the DataSift REST API, can be accessed as a list.

            :param response: HTTP response to wrap
            :type response: :class:`~datasift.requests.DictResponse`
            :param parser: optional parser to overload how the data is loaded
            :type parser: func
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`~datasift.exceptions.DataSiftApiFailure`, :class:`~datasift.exceptions.AuthException`, :class:`requests.exceptions.HTTPError`, :class:`~datasift.exceptions.RateLimitException`
        """
        if response.status_code != 204:
            try:
                data = parser(response.headers, response.text)
            except ValueError as e:
                raise DataSiftApiFailure(u"Unable to decode returned data: %s" % e)
            if "error" in data:
                if response.status_code == 401:
                    raise AuthException(data)
                if response.status_code == 403:
                    if int(response.headers.get("x-ratelimit-cost")) > int(response.headers.get("x-ratelimit-remaining")):
                        raise RateLimitException(data)
                raise DataSiftApiException(DictResponse(response, data))
            response.raise_for_status()
            if isinstance(data, dict):
                r = DictResponse(response, data)
            elif isinstance(data, (list, map)):
                r = ListResponse(response, data)
            outputmapper(r)
            return r

        else:
            # empty dict
            return DictResponse(response, {})

    # Helpers

    def path(self, *args):
        return '/'.join(a.strip('/') for a in args if a)

    def dicts(self, *dicts):
        return dict(kv for d in dicts if d for kv in d.items())


class DatasiftAuth(object):
    """ Internal class to represent an authentication pair.

        :ivar user: Stored username
        :type user: str
        :ivar key: Stored API key
        :type key: str
    """

    def __init__(self, user, key):
        self.user, self.key = user, key

    def __call__(self, request):
        request.headers['Authorization'] = '%s:%s' % (self.user, self.key)
        return request


class DataSiftResponse(object):
    """ Base object wrapper for a response from the DataSift REST API

        :ivar raw: Raw response
        :type raw: list
        :param response: HTTP response to wrap
        :type response: requests.response
        :param data: data to wrap
        :type data: list
    """
    def __init__(self, response, data):
        self._response = response
        self.raw = jsonlib.loads(jsonlib.dumps(data))  # Raw response
        self._insert(data)

    @property
    def status_code(self):
        """ :returns: HTTP Status Code of the Response
            :rtype: int
        """
        return self._response.status_code

    @property
    def headers(self):
        """ :returns: HTTP Headers of the Response
            :rtype: dict
        """
        return dict(self._response.headers)

    @property
    def ratelimits(self):
        """ :returns: Rate Limit headers
            :rtype: dict
        """
        # can't use a dict comprehension because we want python2.6 support
        r = {}
        keys = filter(lambda x: x.startswith("x-ratelimit-"), self.headers.keys())
        for key in keys:
            r[key.replace("x-ratelimit-", "")] = int(self.headers[key])
        return r


class ListResponse(DataSiftResponse, list):
    """ Wrapper for a response from the DataSift REST API, can be accessed as a list. """
    def _insert(self, data):
        self.extend(data)


class DictResponse(DataSiftResponse, dict):
    """ Wrapper for a response from the DataSift REST API, can be accessed as a dict. """
    def _insert(self, data):
        self.update(data)
