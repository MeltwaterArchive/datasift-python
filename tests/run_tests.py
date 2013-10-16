#!/usr/bin/env python
import unittest, os, glob

# Import the tests
from test_user        import TestUser
from test_definition  import TestDefinition
from test_push        import TestPush

# If we've got requests and gevent, also run the gevent streamer tests
try:
    import gevent
    import requests
except ImportError:
    pass
else:
    from test_gevent_stream import TestGeventStream

# Run the tests
unittest.main()
