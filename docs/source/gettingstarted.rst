:orphan:

.. _gettingstarted:

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

Using Response objects
----------------------

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

