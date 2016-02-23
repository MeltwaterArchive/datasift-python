from __future__ import print_function
import time
from datasift import Client

datasift = Client("your username", "your API key")

csdl = '(fb.content any "coffee, tea") AND fb.language in "en"'

print('Validating the CSDL')
print(datasift.pylon.validate(csdl))

print('Compiling the CSDL')
compiled = datasift.pylon.compile(csdl)

print (compiled)

name = 'My analysis recording'

print('Start the recording and wait 10 seconds')
recording = datasift.pylon.start(compiled['hash'], name)
print (recording)

time.sleep(10)

csdl2 = '(fb.content any "coffee, tea, milk") AND fb.language in "en"'
print('Compiling new CSDL')
compiled = datasift.pylon.compile(csdl2)

print (compiled)

print('Updating recording with new filter hash')
datasift.pylon.update(recording['id'], hash=compiled['hash'])

print('Stop the recording')
datasift.pylon.stop(recording['id'])

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
print(datasift.pylon.analyze(recording['id'], analyze_parameters, analyze_filter))

print('Retrive some sample interactions from the recording')
print(datasift.pylon.sample(recording['id']))

print('Retrieve the analysis using get')
print(datasift.pylon.get(recording['id']))
