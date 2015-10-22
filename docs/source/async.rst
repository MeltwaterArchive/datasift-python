:orphan:

.. _async:

Asynchronous Mode
=================

Enabling Async Mode
-------------------

Since version 2.5.0, we've supported an async mode for the client which can be enabled by passing async=True into the Client constructor.

This will swap all of the endpoint functions over to returning a Future with the result in, rather than the result itself.

.. code-block:: python

    >>> import datasift
    >>> client = datasift.Client("myusername", "myapikey", async=True)
    >>> client.usage()
    <Future at 0x7fc32dac3150 state=running>

These will be processed in the background, allowing you to queue up a lot of API requests at once and keep control of your main thread.

They have the same interface as Python 3 futures (https://docs.python.org/3/library/concurrent.futures.html) and have an extra .process() method on them which allows you to get the same result that you'd usually get from the client, including exceptions and datatype transforms.

Basic Example
-------------

If you wanted to validate 5 bits of CSDL in a way that's time sensitive, you might do it like this:

.. code-block:: python

    from __future__ import print_function

    from datasift import Client
    from datasift.exceptions import DataSiftApiException

    from concurrent.futures import as_completed

    client = Client("yourusername", "yourkey", async=True, max_workers=5)

    csdl = [
            'interaction.content contains "python"',
            'this is invalid CSDL',
            'language.tag == "en"',
            'interaction.content any "foo, bar, baz"',
            'interaction.type != "facebook"'
            ]

    # build ourselves a dict of future -> input so we know which one failed
    results = dict([(client.validate(x), x) for x in csdl])


    # add callbacks
    for result in as_completed(results.keys()):
        try:
            result.process()
            print("'%s' was valid CSDL" % results[result])
        except DataSiftApiException:
            print("'%s' was invalid CSDL" % results[result])

When running this, we get the following output::

    'interaction.content any "foo, bar, baz"' was valid CSDL
    'language.tag == "en"' was valid CSDL
    'interaction.content contains "python"' was valid CSDL
    'this is invalid CSDL' was invalid CSDL
    'interaction.type != "facebook"' was valid CSDL

As you can see, this came out in a semi-random order, and will do so whenever you run it, each of these requests is completing as soon as possible, leading to different ordering.

