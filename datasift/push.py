class Push(object):
    def __init__(self, request):
        self.request = request.with_prefix('push')
        self.create = self.create_from_historics

    def validate(self, output_type, output_params):
        """ Check that a subscription is defined correctly.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushvalidate

            :param output_type:   One of DataSift's supported output types, e.g. s3
            :type output_type: str
            :param output_params: The set of parameters required by the specified output_type for docs on all available connectors see http://dev.datasift.com/docs/push/connectors/
            :type output_params: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('validate',
                                 dict(output_type=output_type, output_params=output_params))

    def _create(self, from_hash, stream_or_id, name, output_type, output_params,
                initial_status=None, start=None, end=None):
        params = {
            'name': name,
            'output_type': output_type,
            'output_params': output_params
        }
        if from_hash:
            params['hash'] = stream_or_id
        else:
            params['historics_id'] = stream_or_id

        if initial_status:
            params['initial_status'] = initial_status
        if start:
            params['start'] = start
        if end:
            params['end'] = end

        return self.request.post('create', params)

    def create_from_hash(self, stream, name, output_type, output_params,
                         initial_status=None, start=None, end=None):
        """ Create a new push subscription using a live stream.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushcreate

            :param stream: The hash of a DataSift stream.
            :type stream: str
            :param name: The name to give the newly created subscription
            :type name: str
            :param output_type: One of the supported output types e.g. s3
            :type output_type: str
            :param output_params: The set of parameters required for the given output type
            :type output_params: dict
            :param initial_status: The initial status of the subscription, active, paused or waiting_for_start
            :type initial_status: str
            :param start: Optionally specifies when the subscription should start
            :type start: int
            :param end: Optionally specifies when the subscription should end
            :type end: int
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self._create(True, stream, name, output_type, output_params, initial_status, start, end)

    def create_from_historics(self, historics_id, name, output_type, output_params, initial_status=None, start=None,
                              end=None):
        """ Create a new push subscription using the given Historic ID.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushcreate

            :param historics_id: The ID of a Historics query
            :type historics_id: str
            :param name: The name to give the newly created subscription
            :type name: str
            :param output_type: One of the supported output types e.g. s3
            :type output_type: str
            :param output_params: set of parameters required for the given output type, see dev.datasift.com
            :type output_params: dict
            :param initial_status: The initial status of the subscription, active, paused or waiting_for_start
            :type initial_status: str
            :param start: Optionally specifies when the subscription should start
            :type start: int
            :param end: Optionally specifies when the subscription should end
            :type end: int
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self._create(False, historics_id, name, output_type, output_params, initial_status, start, end)

    def pause(self, subscription_id):
        """ Pause a Subscription and buffer the data for up to one hour.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushpause

            :param subscription_id: id of an existing Push Subscription.
            :type subscription_id: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`

        """
        return self.request.post('pause', data=dict(id=subscription_id))

    def resume(self, subscription_id):
        """ Resume a previously paused Subscription.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushresume

            :param subscription_id: id of an existing Push Subscription.
            :type subscription_id: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`

        """
        return self.request.post('resume', data=dict(id=subscription_id))

    def update(self, subscription_id, output_params, name=None):
        """ Update the name or output parameters for an existing Subscription.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushupdate

            :param subscription_id: id of an existing Push Subscription.
            :type subscription_id: str
            :param output_params: new output parameters for the subscription, see dev.datasift.com
            :type output_params: dict
            :param name: optional new name for the Subscription
            :type name: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {'id': subscription_id, 'output_params': output_params}
        if name:
            params['name'] = name
        return self.request.post('update', params)

    def stop(self, subscription_id):
        """ Stop the given subscription from running.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushstop

            :param subscription_id: id of an existing Push Subscription.
            :type subscription_id: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`

        """
        return self.request.post('stop', data=dict(id=subscription_id))

    def delete(self, subscription_id):
        """ Delete the subscription for the given ID.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushdelete

            :param subscription_id: id of an existing Push Subscription.
            :type subscription_id: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`

        """
        return self.request.post('delete', data=dict(id=subscription_id))

    def log(self, subscription_id=None, page=None, per_page=None, order_by=None, order_dir=None):
        """ Retrieve any messages that have been logged for your subscriptions.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushlog

            :param subscription_id: optional id of an existing Push Subscription, restricts logs to a given subscription if supplied.
            :type subscription_id: str
            :param page: optional page number for pagination
            :type page: int
            :param per_page: optional number of items per page, default 20
            :type per_page: int
            :param order_by: field to order by, default request_time
            :type order_by: str
            :param order_dir: direction to order by, asc or desc, default desc
            :type order_dir: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {}
        if subscription_id:
            params['id'] = subscription_id
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page
        if order_by:
            params['order_by'] = order_by
        if order_dir:
            params['order_dir'] = order_dir

        return self.request.get('log', params=params)

    def get(self, subscription_id=None, stream=None, historics_id=None,
            page=None, per_page=None, order_by=None, order_dir=None,
            include_finished=None):
        """ Show details of the Subscriptions belonging to this user.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/pushget

            :param subscription_id: optional id of an existing Push Subscription
            :type subscription_id: str
            :param hash: optional hash of a live stream
            :type hash: str
            :param playback_id: optional playback id of a Historics query
            :type playback_id: str
            :param page: optional page number for pagination
            :type page: int
            :param per_page: optional number of items per page, default 20
            :type per_page: int
            :param order_by: field to order by, default request_time
            :type order_by: str
            :param order_dir: direction to order by, asc or desc, default desc
            :type order_dir: str
            :param include_finished: boolean indicating if finished Subscriptions for Historics should be included
            :type include_finished: bool
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {}
        if subscription_id:
            params['id'] = subscription_id
        if stream:
            params['hash'] = stream
        if historics_id:
            params['historics_id'] = historics_id
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page
        if order_by:
            params['order_by'] = order_by
        if order_dir:
            params['order_dir'] = order_dir
        if include_finished:
            params['include_finished'] = 1 if include_finished else 0

        return self.request.get('get', params=params)
