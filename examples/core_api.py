from datasift import DataSiftClient
from examples import *

client = DataSiftClient(auth=AUTH)

csdl = 'interaction.content contains "python"'

if client.is_valid(csdl):
    r = client.compile(csdl)
    stream = r['data']['hash']

    print 'Stream %s created' % stream
    print 'It takes %s DPUs' % client.dpu(stream)['data']['dpu']
    print 'Usage INFO \n %s' % client.usage()['data']
    print 'Account balance is %s ' % client.balance()['data']
else:
    print 'Invalid CSDL!!!'