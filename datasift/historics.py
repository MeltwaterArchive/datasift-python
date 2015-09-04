from datasift.exceptions import HistoricSourcesRequired


class Historics(object):
    """ Represents the DataSift Historics REST API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """
    def __init__(self, request):
        self.request = request.with_prefix('historics')

    def prepare(self, hash, start, end, name, sources, sample=None):
        """ Prepare a historics query which can later be started.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicsprepare

            :param hash: The hash of a CSDL create the query for
            :type hash: str
            :param start: when to start querying data from - unix timestamp
            :type start: int
            :param end: when the query should end - unix timestamp
            :type end: int
            :param name: the name of the query
            :type name: str
            :param sources: list of sources  e.g. ['facebook','bitly','tumblr']
            :type sources: list
            :param sample: percentage to sample, either 10 or 100
            :type sample: int
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.HistoricSourcesRequired`, :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        if len(sources) == 0:
            raise HistoricSourcesRequired()
        if not isinstance(sources, list):
            sources = [sources]

        params = {'hash': hash, 'start': start, 'end': end, 'name': name, 'sources': ','.join(sources)}
        if sample:
            params['sample'] = sample
        return self.request.post('prepare', params)

    def start(self, historics_id):
        """ Start the historics job with the given ID.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicsstart

            :param historics_id: hash of the job to start
            :type historics_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('start', data=dict(id=historics_id))

    def update(self, historics_id, name):
        """ Update the name of the given Historics query.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicsupdate

            :param historics_id: playback id of the job to start
            :type historics_id: str
            :param name: new name of the stream
            :type name: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('update', data=dict(id=historics_id, name=name))

    def stop(self, historics_id, reason=''):
        """ Stop an existing Historics query.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicsstop

            :param historics_id: playback id of the job to stop
            :type historics_id: str
            :param reason: optional reason for stopping the job
            :type reason: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('stop', data=dict(id=historics_id, reason=reason))

    def status(self, start, end, sources=None):
        """ Check the data coverage in the Historics archive for a given interval.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicsstatus

            :param start: Unix timestamp for the start time
            :type start: int
            :param end: Unix timestamp for the start time
            :type end: int
            :param sources: list of data sources to include.
            :type sources: list
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {'start': start, 'end': end}
        if sources:
            params['sources'] = ','.join(sources)
        return self.request.get('status', params=params)

    def delete(self, historics_id):
        """ Delete one specified playback query. If the query is currently running, stop it.

            status_code is set to 204 on success

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicsdelete

            :param historics_id: playback id of the query to delete
            :type historics_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('delete', data=dict(id=historics_id))

    def get_for(self, historics_id, with_estimate=None):
        """ Get the historic query for the given ID

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicsget

            :param historics_id: playback id of the query
            :type historics_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.get(historics_id, maximum=None, page=None, with_estimate=with_estimate)

    def get(self, historics_id=None, maximum=None, page=None, with_estimate=None):
        """ Get the historics query with the given ID, if no ID is provided then get a list of historics queries.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicsget

            :param historics_id: (optional) ID of the query to retrieve
            :type historics_id: str
            :param maximum: (optional) maximum number of queries to recieve (default 20)
            :type maximum: int
            :param page: (optional) page to retrieve for paginated queries
            :type page: int
            :param with_estimate: include estimate of completion time in output
            :type with_estimate: bool
            :param historics_id: playback id of the query
            :type historics_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {'id': historics_id}
        if maximum:
            params['max'] = maximum
        if page:
            params['page'] = page

        params['with_estimate'] = 1 if with_estimate else 0
        return self.request.get('get', params=params)

    def pause(self, historics_id, reason=""):
        """ Pause an existing Historics query.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicspause

            :param historics_id: id of the job to pause
            :type historics_id: str
            :param reason: optional reason for pausing it
            :type reason: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {"id": historics_id}
        if reason != "":
            params["reason"] = reason
        return self.request.post('pause', data=params)

    def resume(self, historics_id):
        """ Resume a paused Historics query.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/historicsresume

            :param historics_id: id of the job to resume
            :type historics_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('resume', data=dict(id=historics_id))
