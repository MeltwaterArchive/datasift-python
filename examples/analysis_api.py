from __future__ import print_function
import time
from datasift import Client

datasift = Client("dtsn", "af10bf9030e93bba28af1fec1cf76d9d")

csdl = '(fb.content any "coffee" OR fb.hashtags in "tea") AND fb.language in "en"'

#Validate the analysis CSDL
print(datasift.analysis.validate(csdl))

#Compile the CSDL
compiled = datasift.analysis.compile(csdl)

print (compiled)

name = 'My analysis recording'

#start the recording
datasift.analysis.start(compiled['hash'], name)

#Sleep for 10 seconds
time.sleep(10)

#Stop the recording
datasift.analysis.stop(compiled['hash'])

#$parameters = array(
#	'analysis_type'	=> 'freqDist',
#	'parameters' => array(
#		'threshold'	=> 5,
#		'target'	=> 'fb.author.age'
#	)
#);

analyze_parameters = {'analysis_type': 'freqDist', 'parameters': {'threshold': 5, 'target': 'fb.author.age'}}

print (analyze_parameters)

