# -*- coding: utf8 -*-
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
