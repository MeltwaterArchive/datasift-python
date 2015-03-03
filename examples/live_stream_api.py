# -*- coding: utf8 -*-
from __future__ import print_function
from datasift import Client

ds = Client("your username", "your API key")

@ds.on_delete
def on_delete(interaction):
    print( 'Deleted interaction %s ' % interaction)


@ds.on_open
def on_open():
    print( 'Streaming ready, can start subscribing')
    csdl = 'interaction.content contains "music"'
    stream = ds.compile(csdl)['hash']

    @ds.subscribe(stream)
    def subscribe_to_hash(msg):
        print( msg)


@ds.on_closed
def on_close(wasClean, code, reason):
    print( 'Streaming connection closed')


@ds.on_ds_message
def on_ds_message(msg):
    print( 'DS Message %s' % msg)

#must start stream subscriber
ds.start_stream_subscriber()

