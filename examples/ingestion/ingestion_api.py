from __future__ import print_function
import time
from datasift import Client
import json

datasift = Client("your username", "your API key")

print('Create a gnip managed source to send our data to')

resources = [{'parameters': {'mapping': 'gnip_1'}}]

source = datasift.managed_sources.create('twitter_gnip', 'Python ODP source', resources)

source_id = source['id']

print('Starting delivery for my private source')
datasift.managed_sources.start(source_id)

data = [{'id': '23456234347', 'body': 'This is the body '}]

print('Send the data to the new managed source')
response = datasift.odp.batch(source_id, data)

print(response)

print('Delete the source')
datasift.managed_sources.delete(source_id)
