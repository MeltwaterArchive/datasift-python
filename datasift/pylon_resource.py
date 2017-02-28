
class PylonResource(object):
    """ Represents the DataSift Pylon resource API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """
    def __init__(self, request):
        self.request = request.with_prefix('pylon')

    def get(self, slug, service='facebook', period=None, filter=None):
        """ Get a given Pylon resource

            :param slug: The slug of the resource
            :type slug: str
            :param service: The PYLON service (facebook)
            :type service: str
            :param period: The period for the resource (day, week, month)
            :type period: str
            :param filter: Given filter for the resource
            :type filter: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        params = {}
        if period is not None:
            params['period'] = period
        if filter is not None:
            params['filter'] = filter

        return self.request.get(service + '/resource/' + slug, params)

    def list(self, per_page=None, page=None, service='facebook'):
        """ Get a list of Pylon resources

            :param per_page: How many resources to display per page
            :type per_page: int
            :param page: Which page of resources to display
            :type page: int
            :param service: The PYLON service (facebook)
            :type service: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page

        return self.request.get(service + '/resource', params)
