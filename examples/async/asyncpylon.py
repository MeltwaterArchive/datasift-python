# -*- coding: utf8 -*-

from __future__ import print_function

from datasift import Client
from datasift.exceptions import DataSiftApiException

from concurrent.futures import as_completed

import time
start = time.time()

client = Client("yourusername", "yourkey", async=True, max_workers=5)

recording_hash = "your_recording_hash"

analyze_calls = [
        {'parameters': {'analysis_type': 'freqDist', 'parameters': {'threshold': 10, 'target': 'fb.author.age'}}, 'start': 1445346000, 'end': 1445522340},
        {'parameters': {'analysis_type': 'freqDist', 'parameters': {'threshold': 10, 'target': 'fb.topics.name'}}, 'start': 1445346000, 'end': 1445522340},
        {'parameters': {'analysis_type': 'freqDist', 'parameters': {'threshold': 10, 'target': 'fb.author.gender'}}, 'start': 1445346000, 'end': 1445522340},
        {'parameters': {'analysis_type': 'freqDist', 'parameters': {'threshold': 10, 'target': 'fb.author.region'}}, 'start': 1445346000, 'end': 1445522340},
        {'parameters': {'analysis_type': 'freqDist', 'parameters': {'threshold': 10, 'target': 'fb.media_type'}}, 'start': 1445346000, 'end': 1445522340},
    ]

results = dict([(kwargs['parameters']['parameters']['target'], client.pylon.analyze(recording_hash, **kwargs)) for kwargs in analyze_calls])

for result in results.keys():
    try:
        print(result)
        results[result].process()
        print(results[result].result().text)
    except DataSiftApiException:

        print("The '%s' analysis encountered an error" % results[result])
