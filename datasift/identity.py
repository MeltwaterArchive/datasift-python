

class Identity(object):
    """ Represents the DataSift account/identity REST API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """
    def __init__(self, request):
        self.request = request.with_prefix('account/identity')

    def list(self, label=None, per_page=20, page=1):
        """ Get the existing analysis for a given hash

            :param hash: The optional hash to get recordings with
            :type hash: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """

        params = {'per_page' : per_page, 'page' : page}

        if label:
            params['label'] = label

        return self.request.get('', params)

    def get(self, identity_id):
        """ Get the identity ID

            :param identity_id: The ID of the identity to retrieve
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """

        return self.request.get(identity_id)

    def create_identity(self, label, status=None, master=None):
        """ Create an Identity

            :param label: The label to give this new identity
            :param status: The status of this identity. Will default to 'active' if not set
            :param master: Boolean to represent whether this identity is a master. Defaults to False if not set
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """

        params = {'label' : label}

        if status:
            params['status'] = status
        if master:
            params['master'] = master

        return self.request.post('', params)

    def update_identity(self, identity_id, label=None, status=None, master=None):
        """ Update an Identity

            :param label: The label to give this new identity
            :param status: The status of this identity. Will default to 'active' if not set
            :param master: Boolean to represent whether this identity is a master. Defaults to False if not set
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """

        if label:
            params['label'] = label
        if status:
            params['status'] = status
        if master:
            params['master'] = master

        return self.request.put(identity_id, params)

    def delete_identity(self, identity_id):
        """ Delete an Identity
        
            :param label: The label to give this new identity
            :param status: The status of this identity. Will default to 'active' if not set
            :param master: Boolean to represent whether this identity is a master. Defaults to False if not set
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """

        return self.request.delete(identity_id)

