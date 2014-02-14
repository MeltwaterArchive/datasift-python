DataSift Python Client Library
==============================

This is the official Python library for accessing `DataSift <http://datasift.com/>`_.
See the examples folder for some simple example usage.

All examples and tests use the username and API key in ``config.py``.

Installation
------------

Install with ``pip``::

    pip install datasift-beta

Install from source::

    git clone git@github.com:datasift/datasift-python.git
    cd datasift-python
    python setup.py install


Requirements
^^^^^^^^^^^^

Supports Python 2.6, 2.7 and 3.3.
Uses ``requests``, ``autobahn``, ``six`` and ``twisted``.

License
-------

All code contained in this repository is Copyright 2012-Present MediaSift Ltd.

This code is released under the BSD license. Please see the LICENSE file for
more details.

Changelog
---------

* v.2.0.0 Ground up rewrite.

* v.0.5.7 Fixed issues with buffers on reconnections (2013-06-28)

* v.0.5.6 Fixed broken tests, multistreaming, reconnection timeout (2013-05-03)

* v.0.5.5 Introduced automatic reconnection after 65 seconds of no data or ticks. Solves 'silent disconnect' issue (2013-03-06)

* v.0.5.4 Removed checks for existance of deprecated 'volume_info' field in historics/prepare response (2013-01-18)

* v.0.5.3 Added missing Historic sample size into historic/prepare requests (2012-12-03)

* v.0.5.2 Patch for the missing availability info after Historic/prepare [woozyking](https://github.com/woozyking) (2012-11-28)

* v.0.5.1 Removed unit tests that are no longer required (2012-08-30)

* v.0.5.0 Added support for Historic queries and Push delivery (2012-08-27)

* v.0.4.0 Fixed issues with SSL timeouts & low throughput streams (2012-08-08)

* v.0.3.0 Added SSL support and fixed a reconnection bug (2012-05-16)

  The SSL support is enabled by default and can be disabled by passing false as
  the third parameter to the User constructor, or calling enableSSL(false) on
  the User object.

* v.0.2.0 Fixed the handling of error messages in streams (2012-05-04)

* v.0.1.1 Initial release (2012-03-09)
