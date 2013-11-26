
from exceptions import HistoricSourcesRequired


class HistoricsPreview(object):
    def __init__(self, request):
        self.request = request.with_prefix('preview')

    def create(self, stream, start, parameters, sources, end=None):
        """Create a hitorics preview."""
        if len(sources) == 0:
            raise HistoricSourcesRequired()

        params = {'hash': stream, 'start': start, 'sources': ','.join(sources), 'parameters': ','.join(parameters)}
        if end:
            params['end'] = end
        return self.request.json('create', params)

    def get(self, preview_id):
        """Retrieve a Historics preview."""
        return self.request.get('get', data=dict(id=preview_id))
