
try:
    import ujson as json
except ImportError:
    import json

from datasift_request import req, to_response
from exceptions import HistoricSourcesRequired


class Historics:
    def __init__(self, **config):
        self.config = config

    def prepare(self, stream, start, end, name, sources, sample=None):
        """ Prepare a histroics query which can later be started.

            :hash: The hash of a CSDL create the query for
            :start: when to start querying data from - unix timestamp
            :end: when the query should end - unix timestamp
            :name: the name of the query
            :sources: list of sources  e.g. ['twitter','facebook','bitly','tumblr']
            :sample: either 10 or 100%
        """
        if len(sources) == 0:
            raise HistoricSourcesRequired()

        params = {'hash': stream, 'start': start, 'end': end, 'name': name, 'sources': ','.join(sources)}
        if sample:
            params['sample'] = sample
        return to_response(req('historics/prepare',
                               data=json.dumps(params),
                               headers={'Content-type': 'application/json'},
                               **self.config['request_config']))

    def start(self, historics_id):
        """Start the historics with the given ID."""
        return to_response(req('historics/start', data={'id': historics_id}, **self.config['request_config']))

    def update(self, historics_id, name):
        """Update the name of the given Historics query."""
        return to_response(
            req('historics/update', data={'id': historics_id, 'name': name}, **self.config['request_config']))

    def stop(self, historics_id, reason=''):
        """Stop the historics with the given ID."""
        return to_response(
            req('historics/stop', data={'id': historics_id, 'reason': reason}, **self.config['request_config']))

    def status(self, start, end, sources=None):
        """Check the data coverage in the Historics archive for a given interval."""
        params = {'start': start, 'end': end}
        if sources:
            params['sources'] = ','.join(sources)
        return to_response(req('historics/status', params=params, method='get', **self.config['request_config']))

    def delete(self, historics_id):
        """Delete the historics with the given ID."""
        return to_response(req('historics/delete', data={'id': historics_id}, **self.config['request_config']))

    def get_for(self, historics_id, with_estimate=None):
        """Get the historic query for the given ID"""
        return self.get(historics_id, None, None, with_estimate)

    def get(self, historics_id=None, maximum=None, page=None, with_estimate=None):
        """Get the historics with the given ID, If no ID is provided then get a list of Historic queries."""
        params = {'id': historics_id}
        if maximum:
            params['max'] = maximum
        if page:
            params['page'] = page

        params['with_estimate'] = 1 if with_estimate else 0
        return to_response(req('historics/get', params=params, method='get', **self.config['request_config']))

