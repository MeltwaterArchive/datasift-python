
import examples
from datasift import DataSiftClient

datasift = DataSiftClient(examples.config)

print 'Creating a managed source'
parameters = {
    'likes': True,
    'posts_by_others': True,
    'comments': True
}
resources = [
    {
        'parameters': {
            'url': 'http://www.facebook.com/theguardian',
            'title': 'Some news page',
            'id': 'theguardian'
        }
    }
]

auth = [
    {
        'parameters': {
            'value': 'CAAIUKbXn8xsBAC9uxyezVl4J5xHkKwg9fqhZB1sPJI9LvZAQd6UwHFDJZAkjxSjfEnXzAHzhOVFrHZBKwhOGYghTRMUCZA5iamBN9xK9Yg4oZAxgvzv9j40DAkEsF9XZBbrwcvpJ5ZAL5byL3Ba9oRIYod4AZBfR7nSoQfXbAF7ql94nCBUpzSPCe4DGS40jDys0ZD'
        }
    }
]

source = datasift.managed_source.create('facebook_page', 'My managed source', resources, auth, parameters)
print source

source_id = source.data['id']

print 'Starting delivery for my private source'
print datasift.managed_source.start(source_id)

print 'Updating'
print datasift.managed_source.update(source_id, 'facebook_page', 'Updated source', resources, auth, parameters)

print 'Getting info from DataSift about my page'
print datasift.managed_source.get(source_id)

print 'Fetching logs'
print datasift.managed_source.log(source_id)

print 'Stopping'
print datasift.managed_source.stop(source_id)

print 'Deleting'
print datasift.managed_source.delete(source_id)

