from __future__ import print_function

import examples
from datasift import Client

client = Client(*examples.config)

csdl = 'interaction.content contains "python"'

if client.is_valid(csdl):
    response = client.compile(csdl)
    stream = response['hash']

    print('Stream %s created' % stream)
    print('It takes %s DPUs' % client.dpu(stream)['dpu'])
    print('Usage INFO \n %s' % client.usage())
    print('Account balance is %s ' % client.balance())
else:
    print('Could not validate CSDL')

