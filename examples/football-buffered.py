# encoding: utf-8

# This example consumes 1% of the Twitter stream and outputs a . for each
# interaction received, and an X for each delete notification.
#
# NB: Most of the error handling (exception catching) has been removed for
# the sake of simplicity. Nearly everything in this library may throw
# exceptions, and production code should catch them. See the documentation
# for full details.

import sys, os, time
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]
import config, datasift

print 'Creating user...'
user = datasift.User(config.username, config.api_key)

print 'Creating definition...'
csdl = 'interaction.content contains "football"'
definition = user.create_definition(csdl)
print '  %s' % csdl

print 'Getting buffered interactions...'
print '---'
num = 10
from_id = False
while num > 0:
    interactions = definition.get_buffered(num, from_id)
    for interaction in interactions:
        if 'deleted' in interaction:
            continue
        print 'Type: %s' % (interaction['interaction']['type'])
        print 'Content: %s' % (interaction['interaction']['content'])
        print '--'
        num -= 1

    if num > 0:
        print 'Sleeping (got %d of 10)...' % (10 - num)
        time.sleep(10)
        print '--'

print 'Fetched 10 interactions, we\'re done.'
print