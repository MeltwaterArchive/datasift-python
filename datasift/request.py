"""
Thin wrapper around the requests library.
"""

import json as jsonlib
import requests
import six

from datasift import USER_AGENT, INGESTION_HOST
from datasift.exceptions import DataSiftApiException, DataSiftApiFailure, AuthException, RateLimitException
from datasift.requests_ssl import SslHttpAdapter


def json_decode_wrapper(headers, data):
    return jsonlib.loads(data)


class PartialRequest(object):
    """ Internal class used to represent a yet-to-be-completed request """

    API_SCHEME = 'https'
    API_HOST = 'api.datasift.com'
    API_VERSION = 'v1.5'
    CONTENT_TYPE = 'application/json'
    HEADERS = (
        ('User-Agent', USER_AGENT % API_VERSION),
        ('Content-Type', CONTENT_TYPE)
    )

    def __init__(self, auth, outputmapper, prefix=None, ssl=True, headers=None, timeout=None, proxies=None, verify=True, session=requests.Session(), async=False):
        self.auth = auth
        self.outputmapper = outputmapper
        if not ssl:
            self.API_SCHEME = "http"
        self.prefix = prefix
        self.ssl = ssl
        self.headers = headers
        self.timeout = timeout
        self.proxies = proxies
        self.verify = verify
        self.session = session
        self.adapter = SslHttpAdapter()
        self.session.mount("https://", self.adapter)
        self.async = async

    def get(self, path, params=None, headers=None):
        return self.build_response(self('get', path, params=params, headers=headers), path=path, async=self.async)

    def post(self, path, data=None, headers={'Content-Type': 'application/json'}):
        data = data if isinstance(data, six.string_types) else jsonlib.dumps(data)
        return self.build_response(self('post', path, data=data, headers=headers), path=path, async=self.async)

    def put(self, path, data=None, headers={'Content-Type': 'application/json'}):
        data = data if isinstance(data, six.string_types) else jsonlib.dumps(data)
        return self.build_response(self('put', path, data=data, headers=headers), path=path, async=self.async)

    def delete(self, path, params=None, headers=None, data=None):
        return self.build_response(self('delete', path, params=params, headers=headers, data=data), path=path, async=self.async)

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
        return PartialRequest(self.auth, self.outputmapper, prefix, self.ssl, self.headers, self.timeout, self.proxies, self.verify, self.session, self.async)

    def build_response(self, response, path=None, parser=json_decode_wrapper, async=False):
        """ Builds a List or Dict response object.

            Wrapper for a response from the DataSift REST API, can be accessed as a list.

            :param response: HTTP response to wrap
            :type response: :class:`~datasift.requests.DictResponse`
            :param parser: optional parser to overload how the data is loaded
            :type parser: func
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`~datasift.exceptions.DataSiftApiFailure`, :class:`~datasift.exceptions.AuthException`, :class:`requests.exceptions.HTTPError`, :class:`~datasift.exceptions.RateLimitException`
        """
        if async:
            response.process = lambda: self.build_response(response.result(), path=path, parser=parser, async=False)
            return response
        if response.status_code != 204:
            try:
                data = parser(response.headers, response.text)
            except ValueError as e:
                raise DataSiftApiFailure(u"Unable to decode returned data: %s" % e)
            if "error" in data:
                if response.status_code == 401:
                    raise AuthException(data)
                if response.status_code == 403 or response.status_code == 429:
                    if not response.headers.get("X-RateLimit-Cost"):
                        raise DataSiftApiException(DictResponse(response, data))
                    if int(response.headers.get("X-RateLimit-Cost")) > int(response.headers.get("X-RateLimit-Remaining")):
                        raise RateLimitException(DictResponse(response, data))
                raise DataSiftApiException(DictResponse(response, data))
            response.raise_for_status()
            if isinstance(data, dict):
                r = DictResponse(response, data)
            elif isinstance(data, (list, map)):
                r = ListResponse(response, data)
            self.outputmapper.outputmap(r)
            return r

        else:
            # empty dict
            return DictResponse(response, {})

    # Helpers

    def path(self, *args):
        return '/'.join(a.strip('/') for a in args if a)

    def dicts(self, *dicts):
        return dict(kv for d in dicts if d for kv in d.items())


class IngestRequest(PartialRequest):
    API_HOST = INGESTION_HOST
    API_VERSION = ''


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
