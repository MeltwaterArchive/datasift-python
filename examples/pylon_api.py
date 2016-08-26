from __future__ import print_function
import time
from datasift import Client

datasift = Client("your username", "your API key")

csdl = '(fb.content any "coffee") AND fb.language in "en"'

service = 'facebook'

print('Validating the CSDL')
print(datasift.pylon.validate(csdl))

print('Compiling the CSDL')
compiled = datasift.pylon.compile(csdl)

print (compiled)

name = 'My analysis recording'

print('Start the recording and wait 10 seconds')
datasift.pylon.start(service, compiled['hash'], name)

time.sleep(10)

print('Stop the recording')
datasift.pylon.stop(service, compiled['hash'])

analyze_parameters = {
    'analysis_type': 'freqDist',
    'parameters':
    {
        'threshold': 5,
        'target': 'fb.author.age'
    },
    'child':
    {
        'analysis_type': 'freqDist',
        'parameters':
        {
            'threshold': 2,
            'target': 'fb.author.age'
        }
    }
}

analyze_filter = 'fb.content contains "starbucks"'

print('Hit the analyze end point and return the insights')
print(datasift.pylon.analyze(service, compiled['hash'], analyze_parameters, analyze_filter))

print('Retrive some sample interactions from the recording')
print(datasift.pylon.sample(service, compiled['hash']))

print('Retrieve the analysis using get')
print(datasift.pylon.get(service, compiled['hash']))
