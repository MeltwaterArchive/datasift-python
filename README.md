DataSift Python Client Library
==============================

This is the official Python library for accessing [Datasift](http://datasift.com/). See the examples
folder for some simple example usage.

All examples and tests use the username and API key in config.py.

Installation
------------

The simplest way...

    easy_install datasift

From source...

    python setup.py install


Simple example
--------------

This example looks for anything that contains the word "datasift" and simply
prints the content to the screen as they come in.

```python
import sys, os, config, datasift

class EventHandler(datasift.StreamConsumerEventHandler):
  def on_interaction(self, consumer, data, hash):
    print data['interaction']['content']
  def on_warning(self, consumer, message):
    print 'WARN: %s' % (message)
  def on_error(self, consumer, message):
    print 'ERR: %s' % (message)

user = datasift.User(config.username, config.api_key)
definition = user.create_definition('interaction.content contains "datasift"')
consumer = definition.get_consumer(EventHandler(), 'http')
consumer.consume()
consumer.run_forever()
```

See the DataSift documentation for full details of the data contained within
each interaction. See this page on our developer site for an example tweet:
http://dev.datasift.com/docs/targets/twitter/tweet-output-format

The library will use SSL connections by default. While we recommend using SSL
you may disable it if required by passing False as the third parameter when
creating a user, or by calling enable_ssl(False) on the user object.

Requirements
------------

* Python 2.4+

License
-------

All code contained in this repository is Copyright 2012 MediaSift Ltd.

This code is released under the BSD license. Please see the LICENSE file for
more details.

Changelog
---------

* v.0.3.0 Added SSL support and fixed a reconnection bug (2012-05-16)

  The SSL support is enabled by default and can be disabled by passing false as
  the third parameter to the User constructor, or calling enableSSL(false) on
  the User object.

* v.0.2.0 Fixed the handling of error messages in streams (2012-05-04)

* v.0.1.1 Initial release (2012-03-09)
