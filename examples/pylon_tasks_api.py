from __future__ import print_function
import time
from datasift import Client

datasift = Client("your username", "your API key")

name = 'My analysis recording'

datasift.pylon.list('facebook')

analyze_parameters = {
    'filter': '',
    'analysis_type': 'freqDist',
    'parameters':
    {
        'analysis_type': 'freqDist',
        'parameters': {
            'threshold': 5,
            'target': 'li.activity.type'
        }
    }
}

print('Hit the analyze end point and return the insights')
task = datasift.pylon.task.create(
    service='facebook',
    subscription_id='sub_id',
    name='new task',
    parameters=analyze_parameters
)

print(task)

print('Get the task taht was created')
datasift.pylon.task.get(task['id'])
