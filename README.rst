DataSift Python Client Library
==============================

.. image:: https://travis-ci.org/datasift/datasift-python.svg?branch=master
    :target: https://travis-ci.org/datasift/datasift-python.svg?branch=master

.. image:: https://pypip.in/v/datasift/badge.png
    :target: https://pypi.python.org/pypi/datasift

This is the official Python library for accessing DataSift APIs.

Getting Started
---------------

To get started choose one of our quick start guides:

* `STREAM Quick Start <http://dev.datasift.com/docs/products/stream/quick-start/getting-started-python>`_
* `PYLON for Facebook Topic Data Quick Start <http://dev.datasift.com/docs/products/pylon-fbtd/get-started/getting-started-python>`_

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
* Python 3.4
* Python 3.5
* pypy 2.7

Operating Systems
~~~~~~~~~~~~~~~~~
* Linux
* BSD
* OS X
* Windows 7/8/10 (only with python 2.x) (upstream bug here: <http://twistedmatrix.com/trac/ticket/7626>)

Style Guide
-----------

This code should conform to pep8, with the exception of E501, the 79 character line limit.

It can be style checked with the ``pep8`` module by running ``pep8 --show-source --ignore=E501 datasift/*.py``

Requirements
------------

Supports Python 2.6, 2.7 and 3.3, as well as pypy.
Uses ``requests``, ``autobahn``, ``six``, ``twisted``, ``pyopenssl`` and ``dateutil``.

On non-Windows systems, the ``twisted`` and ``pyopenssl`` packages require the Python and OpenSSL development headers before they can be installed. These are usually provided by distribution package managers in a separate package to the main packages.

Windows users may need to use Python 2.7 due to compatability issues with the `Twisted library <http://www.scriptscoop.net/t/7d436f5544a8/twisted-work-with-python-3-3.html>`_

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

See CHANGELOG file
