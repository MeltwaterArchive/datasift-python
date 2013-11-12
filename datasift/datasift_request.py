import requests
from exceptions import *
from datasift import *


def req(endpoint, auth, params=None, data=None, headers=None, ssl=True, method='post', api_version='v1.1/'):
    """ Make a request to the DataSift API using the key value pair provided by **params to configure the request.

        :api_version:  Default = v1.1 - A string that represents the version of the API e.g. v1 or v1.1
        :ssl:  Default True - A boolean, if true says the request should be performed with SSL i.e. https
        :auth:  Default None - A tuple of the form (username,api_key) - if not provided an AuthError is raised
        :params:  Default {} - A dictionary that is converted to url-encoded key value pairs and appended to the URL
        :headers:  Default {} - A dictionary that is used to set any additional headers for the request
        :data:  Default {} - A dictionary that is used as the payload of a POST request
        :method:  Default post - The string name of the HTTP method to use, Only get and post are supported
    """
    if auth is None or len(auth) != 2 or not auth[0] or not auth[1]:
        raise AuthException('All DataSift API methods require auth info e.g. auth=(username,api_key)')

    if not headers:
        headers = {}

    api_version = api_version if api_version else 'v1.1/'
    headers['Authorization'] = '%s:%s' % auth
    headers['User-Agent'] = USER_AGENT % api_version
    protocol = ('https://' if (SSL_AVAILABLE and ssl) else 'http://')
    url = protocol + API_HOST + api_version + endpoint
    kw = {'headers': headers if headers else {}, 'params': params if params else {}, 'data': data if data else {}}

    if method == 'get':
        return requests.get(url, **kw)
    elif method == 'post':
        return requests.post(url, **kw)


def to_response(r):
    """ Convert an HTTP response to a simple dictionary with data,status_code and response as keys.

    response is the original response object obtained from python-requests, which can be inspected for headers etc
    data is a JSON object created from the response content the API returned, i.e. it is not a string
    status_code is exactly what it says on the tin...
    """
    if r.status_code == 404:
        raise NotFoundException(r.text)
    if r.status_code == 400:
        raise BadRequest(r.json()['error'])
    if r.status_code == 401:
        raise Unauthorized(r.text)
    if r.status_code >= 500:
        raise DataSiftException(r.text)
    return {
        'data': r.json() if r.status_code != 204 else None,
        'statues_code': r.status_code,
        'response': r
    }