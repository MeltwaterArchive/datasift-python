

class Token(object):
    """ Represents the DataSift token API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """

    def __init__(self, request):
        self.request = request.with_prefix('account/identity')

    def list(self, identity_id, per_page=20, page=1):
        """ Get a list of tokens

            :param identity_id: The ID of the identity to retrieve tokens for
            :param per_page: The number of results per page returned
            :param page: The page number of the results
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'per_page': per_page, 'page': page}

        return self.request.get(str(identity_id) + '/token', params)

    def get(self, identity_id, service):
        """ Get a token for a specific identity and service

            :param identity_id: The ID of the identity to retrieve
            :param service: The service that the token is linked to
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        return self.request.get(str(identity_id) + '/token/' + service)

    def create(self, identity_id, service, token):
        """ Create the token

            :param identity_id: The ID of the identity to retrieve
            :param service: The service that the token is linked to
            :param token: The token provided by the the service
            :param expires_at: Set an expiry for this token
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'service': service, 'token': token}

        return self.request.post(str(identity_id) + '/token', params)

    def update(self, identity_id, service, token=None):
        """ Update the token

            :param identity_id: The ID of the identity to retrieve
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {}

        if token:
            params['token'] = token

        return self.request.put(str(identity_id) + '/token/' + service, params)

    def delete(self, identity_id, service):
        """ Delete the token

            :param identity_id: The ID of the identity to retrieve
            :param service: The service that the token is linked to
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        return self.request.delete(str(identity_id) + '/token/' + service)
