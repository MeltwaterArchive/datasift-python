import json

from datasift_request import *


class Historics:
    def __init__(self, **config):
        self.config = config

    def create(self, stream, start, parameters, sources, end=None):
        """Create a hitorics preview.
        """
        if len(sources) == 0:
            raise HistoricSourcesRequired()

        params = {'hash': stream, 'start': start, 'sources': ','.join(sources), 'parameters': ','.join(parameters)}
        if end:
            params['end'] = end
        return to_response(req('preview/create',
                               data=json.dumps(params),
                               headers={'Content-type': 'application/json'},
                               **self.config))

    def get(self, preview_id):
        """Retrieve a Historics preview."""
        return to_response(req('preview/get', data={'id': preview_id}, **self.config))
