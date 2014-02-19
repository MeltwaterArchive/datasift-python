:orphan:

.. _whatsnew:

What's New?
===========

Handling API Errors
-------------------

In the 2.0 revamp of this library it now throws exceptions quite often. This is to help our end users deal with problems in an easier manner.

If you make an invalid request, for example compiling invalid CSDL, you'll get an exception:

.. code-block:: python

    >>> client.compile("interaction.content contains")
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/andi/workspace/datasift-python-dev/datasift/client.py", line 256, in compile
      return self.request.post('compile', data=dict(csdl=csdl))
    File "/home/andi/workspace/datasift-python-dev/datasift/request.py", line 37, in post
      return self.build_response(self('post', path, params=params, headers=headers, data=data), path=path)
    File "/home/andi/workspace/datasift-python-dev/datasift/request.py", line 78, in build_response
      raise DataSiftApiException(Response(response, data))
    datasift.exceptions.DataSiftApiException: At line 1 position 29 we were expecting a text value

The API wasn't happy with the request you sent it, so the client library has raised a DataSiftApiException, these are thrown whenever the server sends back an error, and are designed to help you cope with them easily.

You can deal with these like so:

.. code-block:: python

    from datasift.exceptions import DataSiftApiException

    try:
        hash = client.compile('interaction.content contains python')["hash"]
        print hash
    except DataSiftApiException as e:
        print "API error:", e

When running this, we'll get the following output::

    API error: We are unable to parse this stream. At line 1 position 29 we were expecting a text value

This lets us catch the exception before it tries to use the hash for anything, or before it works out that the response had no hash in it.

Since the exception is a :class:`~datasift.exceptions.DataSiftApiException`, we've got some extra features in it to help you out. If you want more information about why the exception was thrown you can pull the raw interaction out of the exception to look at it:

.. code-block:: python

    >>> e.response
    {u'error': u'We are unable to parse this stream. At line 1 position 29 we were expecting a text value'}
    >>> e.response.status_code
    400
    >>> e.response.headers
    {'x-api-version': '1.1', 'x-ratelimit-remaining': '9930', 'transfer-encoding': 'chunked', 'server': 'nginx/0.8.55', 'connection': 'close', 'x-ratelimit-limit': '10000', 'x-ratelimit-cost': '5', 'date': 'Wed, 29 Jan 2014 16:53:03 GMT', 'p3p': 'CP="CAO PSA"', 'content-type': 'application/json'}


Live Stream Consumption
-----------------------

Also new to this version of the library is the overhauled live stream consumption mode. This uses the autobahn websocket library to stream interactions live from the DataSift API and allows you to work with it by registering callbacks.

The simple example for live streaming looks like this

.. code-block:: python

    from datasift import Client

    client = Client("yourusername", "your API key")

    @client.on_delete
    def on_delete(interaction):
        print "Delete interaction: ", interaction

    @client.on_open
    def on_open():
        print "Stream client set up, subscribing to stream"
        csdl = 'interaction.content contains "DataSift"'
        stream = client.compile(csdl)['hash']

        @client.subscribe(stream)
        def on_interaction(interaction):
            print "Recieved interaction: ", interaction

    @client.on_closed
    def on_close(wasClean, code, reason):
        print "Stream subscriber shutting down because ", reason

    #must start stream subscriber
    client.start_stream_subscriber()

As you can see this new interface uses python decorators to register callbacks for events during the subscription.

