DataSift Python Client Library
==============================

.. image:: https://travis-ci.org/datasift/datasift-python.png
    :target: https://travis-ci.org/datasift/datasift-python

.. image:: https://pypip.in/v/datasift/badge.png
    :target: https://pypi.python.org/pypi/datasift

This is the official Python library for accessing DataSift APIs.

We have recently performed a major update to this library. The previous version is available `here <https://pypi.python.org/pypi/datasift/0.5.7>`_. That version will be supported until 4th September 2014.

Getting Started
---------------

**Read our** `Python Getting Started Guide <http://dev.datasift.com/quickstart/python>`_ **to get started with the DataSift platform.** This guide will take you through creating a `DataSift <http://datasift.com>`_ account, and activating data sources which you will need to do before using the DataSift API.

Many of the examples and API endpoints used in this library require you have enabled certain data sources before you can receive any data (you should do this at `datasift.com/source <https://datasift.com/source>`_). Certain API features, such as `Historics <http://datasift.com/platform/historics/>`_ and `Managed Sources <http://datasift.com/platform/datasources/>`_ will require you have signed up to a monthly subscription before you can access them.

If you are interested in using these features, or would like more information about DataSift, please `get in touch <http://datasift.com/contact-us/>`_!

Installation
------------

Install with ``pip``::

    pip install datasift

Install from source::

    git clone https://github.com/datasift/datasift-python.git
    cd datasift-python
    python setup.py install

Usage
-----

Full documentation is available at http://datasift.github.io/datasift-python


Supported Operating Environment
-------------------------------

This version of the client library has been tested, and is known to work against the following language versions and Operating Systems:

Language versions
~~~~~~~~~~~~~~~~~
* Python 2.6
* Python 2.7
* Python 3.3
* Python 3.4
* pypy 2.7

Operating Systems
~~~~~~~~~~~~~~~~~
* Linux
* BSD
* OS X
* Windows 7/8

Style Guide
-----------

This code should conform to pep8, with the exception of E501, the 79 character line limit.

It can be style checked with the ``pep8`` module by running ``pep8 --show-source --ignore=E501 datasift/*.py``

Requirements
------------

Supports Python 2.6, 2.7 and 3.3, as well as pypy.
Uses ``requests``, ``autobahn``, ``six``, ``twisted``, ``pyopenssl`` and ``dateutil``.

On non-Windows systems, the ``twisted`` and ``pyopenssl`` packages require the Python and OpenSSL development headers before they can be installed. These are usually provided by distribution package managers in a separate package to the main packages.

License
-------

All code contained in this repository is Copyright 2012-Present MediaSift Ltd.

This code is released under the BSD license. Please see the LICENSE file for
more details.

Contributors
------------

* woozyking - patches for Historics/prepare

* glyph from rackspace - assisting with Twisted SSL code


Changelog
---------

* v.2.4.0 Added support for Open Data Processing (ODP) (2015-09-23)

* v.2.3.1 Removed twitter references, made it easier to provide alternative API URL (2015-09-02)

* v.2.1.1 Move to 1.2 of the API (2015-07-22)

* v.2.1.1 Added new historics_id parameter for DPU, fixed bug with POST requests (2015-05-21)

* v.2.1.0 Added support for PYLON (2015-05-15)

* v.2.0.13 Upgraded TLS security when streaming (2015-02-17)

  Big thanks to glyph from rackspace for helping us out with the Twisted SSL code

* v.2.0.11 Added support for pause and resume in historics (2014-08-27)

* v.2.0.10 Bumped to release stable version (2014-08-27)

* v.2.0.9 Bumped to release Dynamic Lists and new Managed Sources endpoints (2014-08-27)

* v.2.0.8 Bumped to release stable version (2014-06-04)

* v.2.0.7 Small bugfix for livestreaming (2014-05-09)

* v.2.0.6 Added windows support for livestreaming (2014-05-09)

* v.2.0.5 Added support for all 3 outputs in pull (2014-04-29)

* v.2.0.4 Upgraded the output mapper date logic to be more robust (2014-03-18)

* v.2.0.3 Fixed secure websockets on OpenSSL >1.0 (2014-02-20)

* v.2.0.2 Improved reconnection logic for livestreaming (2014-02-20)

* v.2.0.1 Fixed disconnect problems in livestreaming on slow streams (2014-02-19)

* v.2.0.0 Ground up rewrite. (2014-02-14)

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
