# encoding: utf-8

# This example consumes 1% of the Twitter stream and outputs a . for each
# interaction received, and an X for each delete notification.
#
# NB: Most of the error handling (exception catching) has been removed for
# the sake of simplicity. Nearly everything in this library may throw
# exceptions, and production code should catch them. See the documentation
# for full details.

import sys, os
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]
import config, datasift

# Reopen stdout without line buffering
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class EventHandler(datasift.StreamConsumerEventHandler):
    def on_connect(self, consumer):
        print 'Connected'
        print '--'

    def on_interaction(self, consumer, interaction, hash):
        sys.stdout.write('.')

    def on_deleted(self, consumer, interaction, hash):
        sys.stdout.write('X')

    def on_warning(self, consumer, message):
        print
        print 'WARN: %s' % (message)

    def on_error(self, consumer, message):
        print
        print 'ERR: %s' % (message)

    def on_disconnect(self, consumer):
        print
        print 'Disconnected'

print 'Creating user...'
user = datasift.User(config.username, config.api_key)

print 'Creating definition...'
csdl = 'interaction.type == "twitter" and interaction.sample < 1.0'
definition = user.create_definition(csdl)
print '  %s' % csdl

print 'Getting the consumer...'
consumer = definition.get_consumer(EventHandler(), 'http')

print 'Consuming...'
print '--'
consumer.consume()

consumer.run_forever()
