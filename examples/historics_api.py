# -*- coding: utf8 -*-
from __future__ import print_function

import time
from datasift import Client


datasift = Client("your username", "your API key")

stream = datasift.compile('interaction.content contains "datasift"')
stream = stream['hash']
start = time.time() - (7200 * 48)  # 48hrs ago
end_time = start + 3600

print('Check the data coverage for the last two hours')
print(datasift.historics.status(start, end_time))

print('Preparing')
historics = datasift.historics.prepare(stream, start, end_time, 'My python historics', ['tumblr'])

print(historics)

historics_id = historics['id']

print('Creating push subscription for historics')
create_params = {
        'name': 'My awesome push subscription',
        'initial_status': 'active',
        'playback_id': stream,
        'start': time.time(),
        'end': time.time() + 320
    }
print('Creating subscription')
subscription = datasift.push.create_from_historics(historics_id, 'Python push', 'pull', {})
print(subscription)

print("Starting historics %s" % subscription)
print(datasift.historics.start(historics_id))

print('Updating historics')
print(datasift.historics.update(historics_id, 'The new name of my historics'))

print('Get info for the historics')
print(datasift.historics.get(historics_id))

print('Getting info for all my historics')
print(datasift.historics.get())

print('Stopping historics')
print(datasift.historics.stop(historics_id))

print('Deleting historics')
print(datasift.historics.delete(historics_id))

