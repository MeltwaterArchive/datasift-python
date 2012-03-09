# encoding: utf-8

# This simple example demonstrates how to consume a stream using the stream
# hash. You can pass multiple hashes to this script to consume multiple
# streams through the same connection.
# 
# NB: Most of the error handling (exception catching) has been removed for
# the sake of simplicity. Nearly everything in this library may throw
# exceptions, and production code should catch them. See the documentation
# for full details.

import sys, os
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]
import config, datasift

if len(sys.argv) < 2:
    print 'ERR: Please specify at least one stream hash to consume!'
    sys.exit()

class EventHandler(datasift.StreamConsumerEventHandler):
    def on_connect(self, consumer):
        print 'Connected'
        print '--'

    def on_interaction(self, consumer, interaction, hash):
        print '[%s]' % hash, interaction['interaction']['content']
        print '--'

    def on_deleted(self, consumer, interaction, hash):
        print '[%s]' % hash, 'Deleted:', interaction['interaction']['id']
        print '--'

    def on_warning(self, consumer, message):
        print 'WARN: %s' % (message)

    def on_error(self, consumer, message):
        print 'ERR: %s' % (message)

    def on_disconnect(self, consumer):
        print 'Disconnected'

print 'Creating user...'
user = datasift.User(config.username, config.api_key)

print 'Getting the consumer...'
consumer = user.get_multi_consumer(sys.argv[1:], EventHandler(), 'http')

print 'Consuming...'
print '--'
consumer.consume()

consumer.run_forever()
