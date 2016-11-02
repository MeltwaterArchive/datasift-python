from __future__ import print_function
import time
from datasift import Client

datasift = Client("USERNAME", "API_KEY")

csdl = '(fb.content any "coffee, tea, sugar") AND fb.language in "en"'

service = 'facebook'

print('Validating the CSDL')
print(datasift.pylon.validate(csdl, service=service))

print('Compiling the CSDL')
compiled = datasift.pylon.compile(csdl, service=service)

print(compiled)

name = 'My analysis recording'

print('Start the recording and wait 10 seconds')
results = datasift.pylon.start(compiled['hash'], name, service=service)

recording_id = results['id']

time.sleep(10)

csdl2 = '(fb.content any "coffee, tea, milk") AND fb.language in "en"'
print('Compiling new CSDL')
compiled = datasift.pylon.compile(csdl2)

print (compiled)

print('Updating recording with new filter hash')
datasift.pylon.update(recording['id'], hash=compiled['hash'])

print('Stop the recording')
datasift.pylon.stop(recording_id, service=service)

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
print(datasift.pylon.analyze(recording_id, analyze_parameters, analyze_filter, service=service))

print('Retrive some sample interactions from the recording')
print(datasift.pylon.sample(recording_id, service=service))

print('Retrieve the recording details using get')
print(datasift.pylon.get(recording_id, service=service))

print('List all recordings')
print(datasift.pylon.list(service=service))
