
import time
import examples
from datasift import Client

datasift = Client(examples.config)

csdl = 'interaction.content contains "python"'

s3_params = {
    'bucket': 'apitests',
    'directory': 'ruby',
    'acl': 'private',
    'auth': {
        'access_key': 'AKIAIINK5C4FH75RSWNA',
        'secret_key': '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'
    },
    'delivery_frequency': 0,
    'max_size': 10485760,
    'file_prefix': 'DataSift',
}

res = datasift.push.validate('s3', s3_params)
print res

stream = datasift.compile(csdl)
print 'Creating a pull subscription from stream ==> %s' % stream.data['hash']
print stream
subscription = datasift.push.create_from_hash(stream.data['hash'], 'My Python Pull subscription', 'pull', {})
print subscription

time.sleep(30)


def on_interaction(i):
    print 'on_interaction ==> %s' % i

datasift.pull(subscription.data['id'], on_interaction=on_interaction)

