
import examples
from datasift import DataSiftClient

client = DataSiftClient(examples.config)

csdl = 'interaction.content contains "python"'

if client.is_valid(csdl):
    response = client.compile(csdl)
    stream = response.data['hash']

    print 'Stream %s created' % stream
    print 'It takes %s DPUs' % client.dpu(stream).data['dpu']
    print 'Usage INFO \n %s' % client.usage().data
    print 'Account balance is %s ' % client.balance().data
else:
    print 'Could not validate CSDL'

