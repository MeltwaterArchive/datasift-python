

class Limit(object):
    """ Represents the DataSift limit API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """

    def __init__(self, request):
        self.request = request.with_prefix('account/identity')

    def get(self, identity_id, service):
        """ Get the limit for the given identity and service

            :param identity_id: The ID of the identity to retrieve
            :param service: The service that the limit is linked to
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        return self.request.get(str(identity_id) + '/limit/' + service)

    def list(self, service, per_page=20, page=1):
        """ Get a list of limits for the given service

            :param service: The service that the limit is linked to
            :param per_page: The number of results per page returned
            :param page: The page number of the results
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'per_page': per_page, 'page': page}

        return self.request.get('limit/' + service, params)

    def create(self, identity_id, service, total_allowance=None, analyze_queries=None):
        """ Create the limit

            :param identity_id: The ID of the identity to retrieve
            :param service: The service that the token is linked to
            :param total_allowance: The total allowance for this token's limit
            :param analyze_queries: The number of analyze calls
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'service': service}

        if total_allowance is not None:
            params['total_allowance'] = total_allowance
        if analyze_queries is not None:
            params['analyze_queries'] = analyze_queries

        return self.request.post(str(identity_id) + '/limit/', params)

    def update(self, identity_id, service, total_allowance=None, analyze_queries=None):
        """ Update the limit

            :param identity_id: The ID of the identity to retrieve
            :param service: The service that the token is linked to
            :param total_allowance: The total allowance for this token's limit
            :param analyze_queries: The number of analyze calls
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'service': service}
        if total_allowance is not None:
            params['total_allowance'] = total_allowance
        if analyze_queries is not None:
            params['analyze_queries'] = analyze_queries
        return self.request.put(str(identity_id) + '/limit/' + service, params)

    def delete(self, identity_id, service):
        """ Delete the limit for the given identity and service

            :param identity_id: The ID of the identity to retrieve
            :param service: The service that the token is linked to
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        return self.request.delete(str(identity_id) + '/limit/' + service)
