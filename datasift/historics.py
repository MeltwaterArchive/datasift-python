from datasift.exceptions import HistoricSourcesRequired


class Historics(object):
    """Class which represents the DataSift Historics REST API and provides the ability to query it."""
    def __init__(self, request):
        self.request = request.with_prefix('historics')

    def prepare(self, stream, start, end, name, sources, sample=None):
        """ Prepare a histroics query which can later be started.

            :param hash: The hash of a CSDL create the query for
            :type hash: str
            :param start: when to start querying data from - unix timestamp
            :type start: int
            :param end: when the query should end - unix timestamp
            :type end: int
            :param name: the name of the query
            :type name: str
            :param sources: list of sources  e.g. ['twitter','facebook','bitly','tumblr']
            :type sources: list
            :param sample: percentage to sample, either 10 or 100
            :type sample: int
        """
        if len(sources) == 0:
            raise HistoricSourcesRequired()

        params = {'hash': stream, 'start': start, 'end': end, 'name': name, 'sources': ','.join(sources)}
        if sample:
            params['sample'] = sample
        return self.request.json('prepare', params)

    def start(self, historics_id):
        """ Start the historics job with the given ID.

            :param historics_id: hash of the job to start
            :type historics_id: str
            :return: dict of REST API output with headers attached
            :rtype: request.Response
        """
        return self.request.post('start', data=dict(id=historics_id))

    def update(self, historics_id, name):
        """Update the name of the given Historics query."""
        return self.request.post('update', data=dict(id=historics_id, name=name))

    def stop(self, historics_id, reason=''):
        """Stop the historics with the given ID."""
        return self.request.post('stop', data=dict(id=historics_id, reason=reason))

    def status(self, start, end, sources=None):
        """Check the data coverage in the Historics archive for a given interval."""
        params = {'start': start, 'end': end}
        if sources:
            params['sources'] = ','.join(sources)
        return self.request.get('status', params=params)

    def delete(self, historics_id):
        """Delete the historics with the given ID."""
        return self.request.post('delete', data=dict(id=historics_id))

    def get_for(self, historics_id, with_estimate=None):
        """Get the historic query for the given ID"""
        return self.get(historics_id, maximum=None, page=None, with_estimate=with_estimate)

    def get(self, historics_id=None, maximum=None, page=None, with_estimate=None):
        """Get the historics with the given ID, If no ID is provided then get a list of Historic queries."""
        params = {'id': historics_id}
        if maximum:
            params['max'] = maximum
        if page:
            params['page'] = page

        params['with_estimate'] = 1 if with_estimate else 0
        return self.request.get('get', params=params)
