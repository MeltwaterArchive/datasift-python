

class Identity(object):
    """ Represents the identity API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """
    def __init__(self, request):
        self.request = request.with_prefix('account/identity')

    def list(self, label=None, per_page=20, page=1):
        """ Get a list of identities that have been created

            :param per_page: The number of results per page returned
            :type per_page: int
            :param page: The page number of the results
            :type page: int
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'per_page': per_page, 'page': page}

        if label:
            params['label'] = label

        return self.request.get('', params)

    def get(self, id):
        """ Get the identity ID

            :param identity_id: The ID of the identity to retrieve
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        return self.request.get(str(id))

    def create(self, label, status=None, master=None):
        """ Create an Identity

            :param label: The label to give this new identity
            :param status: The status of this identity. Default: 'active'
            :param master: Represents whether this identity is a master.
                Default: False
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'label': label}

        if status:
            params['status'] = status
        if master:
            params['master'] = master

        return self.request.post('', params)

    def update(self, id, label=None, status=None, master=None):
        """ Update an Identity

            :param label: The label to give this new identity
            :param status: The status of this identity. Default: 'active'
            :param master: Represents whether this identity is a master.
                Default: False
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {}

        if label:
            params['label'] = label
        if status:
            params['status'] = status
        if master:
            params['master'] = master

        return self.request.put(str(id), params)

    def delete(self, id):
        """ Delete an Identity

            :param label: The label to give this new identity
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        return self.request.delete(str(id))
