import json

from datasift_request import *


class ManagedSources:
    def __init__(self, **config):
        self.config = config

    def create(self, source_type, name, resources, auth=None, parameters=None):
        """ Create a managed source

            :source_type:   A data source name e.g. facebook_page, googleplus, instagram, yammer
            :name: A name to use to identify the managed source being created
            :resources: A list of source-specific config.
            :auth: A list of source-specific authentication info for the given source type
            :parameters: An object with config information on how to treat each resource
        """
        params = {'source_type': source_type, 'name': name, 'resources': resources}
        if auth:
            params['auth'] = auth
        if parameters:
            params['parameters'] = parameters

        return to_response(req('source/create', data=json.dumps(params), headers={'Content-type': 'application/json'},
                               **self.config['request_config']))

    def update(self, source_id, source_type, name, resources, auth=None, parameters=None):
        """ Update a managed source

            :source_type:   A data source name e.g. facebook_page, googleplus, instagram, yammer
            :name: A name to use to identify the managed source being created
            :resources: A list of source-specific config.
            :auth: A list of source-specific authentication info for the given source type
            :parameters: An object with config information on how to treat each resource
        """
        params = {'id': source_id, 'source_type': source_type, 'name': name, 'resources': resources}
        if auth:
            params['auth'] = auth
        if parameters:
            params['parameters'] = parameters

        return to_response(req('source/update', data=json.dumps(params), headers={'Content-type': 'application/json'},
                               **self.config['request_config']))

    def start(self, source_id):
        """Start consuming from a managed source."""
        return to_response(req('source/start', data={'id': source_id}, **self.config['request_config']))

    def stop(self, source_id):
        """Stop a managed source."""
        return to_response(req('source/stop', data={'id': source_id}, **self.config['request_config']))

    def delete(self, source_id):
        """Delete a managed source."""
        return to_response(req('source/delete', data={'id': source_id}, **self.config['request_config']))

    def logs_for(self, source_id, page=None, per_page=None):
        """Retrieve any messages that have been logged for this managed source."""
        params = {'id': source_id}
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page

        return to_response(req('source/log', params=params, method='get', **self.config['request_config']))

    def get_source(self, source_id, source_type=None, page=None, per_page=None):
        self.get(source_id, source_type, page, per_page)

    def get(self, source_id=None, source_type=None, page=None, per_page=None):
        """Get a specific managed source or a list of them."""
        params = {}
        if source_type:
            params['source_type'] = source_type
        if source_id:
            params['id'] = source_id
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page

        return to_response(req('source/get', params=params, method='get', **self.config['request_config']))
