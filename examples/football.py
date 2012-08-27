# encoding: utf-8

# This example constructs a DataSift_Definition object with CSDL that looks
# for anything containing the word "football". It then gets an HTTP
# consumer for that definition and displays matching interactions to the
# screen as they come in. It will display 10 interactions and then stop.
#
# NB: Most of the error handling (exception catching) has been removed for
# the sake of simplicity. Nearly everything in this library may throw
# exceptions, and production code should catch them. See the documentation
# for full details.

import sys, os
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]
import config, datasift

class EventHandler(datasift.StreamConsumerEventHandler):
    def __init__(self):
        self.num = 10

    def on_connect(self, consumer):
        print 'Connected'
        print '--'

    def on_interaction(self, consumer, interaction, hash):
        print 'Type:', interaction['interaction']['type']
        print 'Content:', interaction['interaction']['content'].encode('ascii', 'replace')
        print '--'
        self.num -= 1
        if self.num == 0:
            print 'Stopping consumer...'
            consumer.stop()

    def on_deleted(self, consumer, interaction, hash):
        print 'Delete request for interaction %d of type %s.' % (interaction['interaction']['id'], interaction['interaction']['type'])
        print 'Please delete it from your archive.'
        print '--'

    def on_warning(self, consumer, message):
        print 'WARN: %s' % (message)
        print '--'

    def on_error(self, consumer, message):
        print 'ERR: %s' % (message)
        print '--'

    def on_status(self, consumer, status, data):
        print 'STATUS: %s' % (status)
        print '--'

    def on_disconnect(self, consumer):
        print 'Disconnected'

print 'Creating user...'
user = datasift.User(config.username, config.api_key)

print 'Creating definition...'
csdl = 'interaction.content contains "football" and language.tag == "en"'
definition = user.create_definition(csdl)
print '  %s' % csdl

print 'Getting the consumer...'
consumer = definition.get_consumer(EventHandler(), 'http')

print 'Consuming...'
print '--'
consumer.consume()

consumer.run_forever()
