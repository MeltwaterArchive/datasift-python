:orphan:

.. _gettingstarted:

Getting Started
===============

This page shows general use of the client, suitable for a beginner.

Building the Client Object
--------------------------

Here's a small example using the core API:

.. code-block:: python

    from datasift import Client

    client = Client("mydatasiftusername", "mydatasiftapikey")

    print client.usage()

If you haven't been doing much, this'll output something boring like:

.. code-block:: python

    {'streams': {}, 'start': datetime.datetime(2014, 2, 11, 11, 25), 'end': datetime.datetime(2014, 2, 11, 12, 25)}

As you can see, :func:`~datasift.client.Client.usage` returns what looks like a dictionary object which contains python datetimes for ease of use.

This is actually a :class:`~datasift.request.Response` object which can be used as a dictionary, but includes extra information such as HTTP status code and headers.

Using Response objects
----------------------

This time, let's store the response object so we can do things with it:

.. code-block:: python

    usage = client.usage()

If you're used to using the old library, or our API directly, you can get the unconverted response using the .raw property of this object:

.. code-block:: python

    >>> usage.raw
    {'streams': {}, 'start': 'Tue, 11 Feb 2014 11:25:00 +0000', 'end': 'Tue, 11 Feb 2014 12:25:00 +0000'}


If you want to check your rate limits, you can use the .ratelimits property of this object:

.. code-block:: python

    >>> usage.ratelimits
    {'limit': 10000, 'remaining': 9785, 'cost': 25}

For the full headers you can use .headers:

.. code-block:: python

    >>> usage.headers
    {'x-served-by': 'ded2584', 'x-api-version': '1.1', 'x-cache-control': 'max-age=300, must-revalidate', 'transfer-encoding': 'chunked', 'p3p': 'CP="CAO PSA"', 'connection': 'close', 'content-type': 'application/json', 'x-ratelimit-cost': '25', 'date': 'Tue, 11 Feb 2014 12:28:39 GMT', 'server': 'nginx/0.8.55', 'x-ratelimit-remaining': '9785', 'x-ratelimit-limit': '10000'}

Or if you want to do things with the data, you can work with it as you'd use a dict:

.. code-block:: python

    >>> usage["end"] - usage["start"]
    datetime.timedelta(0, 3600)

