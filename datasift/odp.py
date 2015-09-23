import requests
import json
from datasift.exceptions import BadRequest


class Odp(object):
    """ Represents the DataSift Open Data Processing REST API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """

    def __init__(self, request):
        self.request = request

    def batch(self, source_id, data):
        """ Upload data to the given soruce

            :param source_id: The ID of the source to upload to
            :type source_id: str
            :param data: The data to upload to the source
            :type data: list
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`,
                :class:`~datasift.exceptions.BadRequest`
        """
        if type(data) is not list or type(data[0]) is not dict:
            raise BadRequest("Ingestion data must be a list of dicts")
        data = "\r\n".join(map(json.dumps, data))
        return self.request.post(source_id, data, {'Accept-Encoding': 'application/text'})
