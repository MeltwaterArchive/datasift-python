from __future__ import print_function
from datasift import Client

datasift = Client("USERNAME", "API_KEY")

name = 'Example Analysis Task'
service = 'facebook'

#datasift.pylon.list(service=service)

analyze_parameters = {
    'filter': '',
    'analysis_type': 'freqDist',
    'parameters':
    {
        'analysis_type': 'freqDist',
        'parameters': {
            'threshold': 5,
            'target': 'fb.activity.type'
        }
    }
}

print('Create an analysis task')
task = datasift.pylon.task.create(
    subscription_id='SUBSCRIPTION_ID',
    name=name,
    parameters=analyze_parameters,
    service=service
)
print(task)

print('Get the task that was created')
results = datasift.pylon.task.get(task['id'], service=service)
print(results)
