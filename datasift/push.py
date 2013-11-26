
import json, requests

from functools import partial
from datasift.datasift_request import Response


class Push(object):
    def __init__(self, request):
        self.request = request.with_prefix('push')

    def validate(self, output_type, output_params):
        """ Check that a subscription is defined correctly.
            :output_type:   One of DataSift's supported output types, e.g. s3
            :output_params: The set of parameters required by the specified output_type for docs on all available
                            connectors see http://dev.datasift.com/docs/push/connectors/
        """
        return self.request.json('validate',
                dict(output_type=output_type, output_params=output_params))

    def create(self, from_hash, stream_or_id, name, output_type, output_params,
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

        return self.request.json('create', params)

    def create_from_hash(self, stream, name, output_type, output_params,
            initial_status=None, start=None, end=None):
        """Create a new push subscription using a live stream.

            :stream: The hash of a DataSift stream.
            :name: The name to give the newly created subscription
            :output_type: One of the supported output types e.g. s3
            :output_params: The set of parameters required for the given output type
            :initial_status: The initial status of the subscription, active, paused or waiting_for_start
            :start: Optionally specifies when the subscription should start
            :end: Optionally specifies when the subscription should end
        """
        return self.create(True, stream, name, output_type, output_params, initial_status, start, end)

    def create_from_historics(self, historics_id, name, output_type, output_params, initial_status=None, start=None,
                              end=None):
        """Create a new push subscription using the given Historic ID.

            :historics_id: The ID of a Historics query..
            :name: The name to give the newly created subscription
            :output_type: One of the supported output types e.g. s3
            :output_params: The set of parameters required for the given output type
            :initial_status: The initial status of the subscription, active, paused or waiting_for_start
            :start: Optionally specifies when the subscription should start
            :end: Optionally specifies when the subscription should end
        """
        return self.create(False, historics_id, name, output_type, output_params, initial_status, start, end)

    def pause(self, subscription_id):
        """Pause the subscription for the given ID."""
        return self.request.post('pause', data=dict(id=subscription_id))

    def resume(self, subscription_id):
        """Resumed a previously paused subscription for the given ID."""
        return self.request.post('resume', data=dict(id=subscription_id))

    def update(self, subscription_id, output_params, name=None):
        params = {'subscription_id': subscription_id, 'output_params': output_params}
        if name:
            params['name'] = name
        return self.request.json('update', params)

    def stop(self, subscription_id):
        """Stop the given subscription from running."""
        return self.request.post('stop', data=dict(id=subscription_id))

    def delete(self, subscription_id):
        """Delete the subscription for the given ID."""
        return self.request.post('delete', data=dict(id=subscription_id))

    def logs_for(self, subscription_id, page=None, per_page=None, order_by=None, order_dir=None):
        """Get logs for a given subscription ID."""
        return self.log(subscription_id, page, per_page, order_by, order_dir)

    def log(self, subscription_id=None, page=None, per_page=None, order_by=None, order_dir=None):
        """Retrieve any messages that have been logged for your subscriptions."""
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

    def get_subscription(self, subscription_id, stream=None, historics_id=None, page=None, per_page=None, order_by=None,
                         order_dir=None, include_finished=None):
        """Get all available info for the given subscription ID."""
        return self.get(subscription_id, stream, historics_id, page, per_page, order_by, order_dir, include_finished)

    def get(self, subscription_id=None, stream=None, historics_id=None, page=None, per_page=None, order_by=None,
            order_dir=None, include_finished=None):
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
            params['include_finished'] = include_finished

        return self.request.get('get', params=params)

    def pull(self, subscription_id, size=None, cursor=None, on_interaction=None):
        """Pulls a series of interactions from the queue for the given subscription ID.

            :subscription_id: The ID of the subscription to pull interactions for
            :size: the max amount of data to pull in bytes
            :cursor: an ID to use as the point in the queue from which to start fetching data
            :on_interaction: If provided this should be a function. It will be invoked once for each interaction pulled
            from the queue. If you're planning to iterate over each interaction it is more efficient provide this
            doing so will avoid the need for you to iterate over the same data the client already iterates over.
        """
        params = {'id': subscription_id}
        if size:
            params['size'] = size
        if cursor:
            params['cursor'] = cursor
        # Use the requests API directly for this:
        r = requests.get('%s://%s/v1/push/pull' % (self.request.API_SCHEME, self.request.API_HOST),
                params=params,
                verify=self.request.verify,
                timeout=self.request.timeout,
                proxies=self.request.proxies,
                headers=self.request.dicts(self.request.headers, self.request.USER_AGENT))
        return Response(r, partial(self._parse_interactions, on_interaction=on_interaction))

    def _parse_interactions(self, data, on_interaction=None):
        interactions = []
        for line in data.strip().split('\n'):
            if line:
                i = json.loads(line)
                if on_interaction:
                    on_interaction(i)
                interactions.append(i)
        return interactions


