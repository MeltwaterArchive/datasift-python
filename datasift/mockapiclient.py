# encoding: utf-8
class MockApiClient():

    _response = None

    def set_response(self, response):
        self._response = response

    def call(self, username, api_key, endpoint, params = {}, user_agent = 'DataSiftPython/1.0'):
        return self._response
