from __future__ import print_function
import time
from datasift import Client

datasift = Client("your username", "your API key")

csdl = '(fb.content any "coffee" OR fb.hashtags in "tea") AND fb.language in "en"'

print('Validating the CSDL')
print(datasift.analysis.validate(csdl))

print('Compiling the CSDL')
compiled = datasift.analysis.compile(csdl)

print (compiled)

name = 'My analysis recording'

print('Start the recording and wait 10 seconds')
datasift.analysis.start(compiled['hash'], name)

time.sleep(10)

print('Stop the recording')
datasift.analysis.stop(compiled['hash'])

analyze_parameters = {'analysis_type': 'freqDist', 'parameters': {'threshold': 5, 'target': 'fb.author.age'}}

analyze_filter = 'fb.content contains "starbucks"'

print('Hit the analyze end point and return the insights')
print (datasift.analysis.analyze(compiled['hash'], analyze_parameters, analyze_filter))

print('Retrieve the analysis using get')
print(datasift.analysis.get(compiled['hash']))
