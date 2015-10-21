from __future__ import print_function
import time
from datasift import Client

datasift = Client("your username", "your API key")

print('Retrieve account usage information')
print(datasift.account.usage())
