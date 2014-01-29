Welcome to the datasift Python module
=====================================

Contents:

.. toctree::
   :maxdepth: 2

   index
   datasift

Getting Started
===============

This page shows general use of the client, suitable for a beginner.

Building the Client Object
--------------------------

Here's a small example using the core API:

.. code-block:: python

    from datasift import DataSiftConfig, DataSiftClient

    client = DataSiftClient(DataSiftConfig("mydatasiftusername", "mydatasiftapikey")

    print client.usage()

If you haven't been doing much, this'll output something boring like:

.. code-block:: python

    {u'start': datetime.datetime(2014, 1, 29, 15, 20), u'end': datetime.datetime(2014, 1, 29, 16, 20), u'streams': {}}

As you can see, client.usage() returns what looks like a dictionary object which contains python datetimes for ease of use.

This is actually a :class:`~datasift.request.Response` object which can be used as a dictionary, but includes extra information such as HTTP status code and headers.

Using the Response objects
--------------------------

This time, let's store the response object so we can do things with it:

.. code-block:: python

    usage = client.usage()

If you're used to using the old library, or our API directly, you can get the raw JSON using the .raw property of this object:

.. code-block:: python

    >>> usage.raw
    {u'start': u'Wed, 29 Jan 2014 15:25:00 +0000', u'end': u'Wed, 29 Jan 2014 16:25:00 +0000', u'streams': {}}

If you want to check your rate limits, you can read the headers on this object:

.. code-block:: python

    >>> usage.headers
    {'x-api-version': '1.1', 'x-ratelimit-remaining': '9950', 'x-served-by': 'ded2584', 'transfer-encoding': 'chunked', 'server': 'nginx/0.8.55', 'connection': 'close', 'x-ratelimit-limit': '10000', 'x-ratelimit-cost': '25', 'date': 'Wed, 29 Jan 2014 16:28:45 GMT', 'p3p': 'CP="CAO PSA"', 'content-type': 'application/json', 'x-cache-control': 'max-age=300, must-revalidate'}


Or if you want to do things with the data, you can work with it as you'd use a dict:

.. code-block:: python

    >>> usage["end"] - usage["start"]
    datetime.timedelta(0, 3600)

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

Also new to this version of the library is the live stream consumption mode. This uses the autobahn websocket library to stream interactions live from the DataSift API and allows you to work with it by registering callbacks.

The simple example for live streaming looks like this

.. code-block:: python

    from datasift import DataSiftClient, DataSiftConfig

    client = DataSiftClient(DataSiftConfig("yourusername", "your API key")

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

As you can see this new interface uses python decorators to register callbacks for events during the subscription.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

