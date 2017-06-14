# -*- coding: utf-8 -*-

"""
DataSift Python Client Library
==============================

This is the official Python library for accessing `DataSift <http://datasift.com/>`_.
See the examples folder for some simple example usage.

All examples and tests use the username and API key in ``config.py``.

DataSift Platform Documentation: http://dev.datasift.com/docs/


Installation
------------

Install with ``pip``::

    pip install datasift

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

"""

__author__ = "opensource@datasift.com"
__status__ = "stable"
__version__ = "2.11.0"
__date__ = "14th Jun 2017"

# -----------------------------------------------------------------------------
# Module constants
# -----------------------------------------------------------------------------
USER_AGENT = 'DataSift/%s Python/' + __version__
WEBSOCKET_HOST = 'stream.datasift.com'
API_HOST = 'api.datasift.com/'
INGESTION_HOST = 'in.datasift.com/'

from datasift.client import Client
