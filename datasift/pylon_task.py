
class PylonTask(object):
    """ Represents the DataSift Pylon task API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """
    def __init__(self, request):
        self.request = request.with_prefix('pylon')

    def get(self, service, id):
        """ Get a given Pylon task

            :param service: The PYLON service (facebook, linkedin)
            :type service: str
            :param id: The ID of the task
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.get(service + '/task/' + id)

    def list(self, service, per_page=None, page=None, status=None):
        """ Get a list of Pylon tasks

            :param service: The PYLON service (facebook, linkedin)
            :type service: str
            :param per_page: How many tasks to display per page
            :type per_page: int
            :param page: Which page of tasks to display
            :type page: int
            :param status: The status of the tasks to list
            :type page: string
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
        if status:
            params['status'] = status

        return self.request.get(service + '/task', params)

    def create(self, service, subscription_id, name, parameters, type='analysis'):
        """ Create a PYLON task

            :param service: The PYLON service (facebook, linkedin)
            :type service: str
            :param subscription_id: The ID of the recording to create the task for
            :type subscription_id: str
            :param name: The name of the new task
            :type name: str
            :param parameters: The parameters for this task
            :type parameters: dict
            :param type: The type of analysis to create, currently only 'analysis' is accepted
            :type type: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {
            'subscription_id': subscription_id,
            'name': name,
            'parameters': parameters,
            'type': type
        }

        return self.request.post(service + '/task/', params)
