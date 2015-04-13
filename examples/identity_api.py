from __future__ import print_function
import time
from datasift import Client
import json

datasift = Client("CS_10N", "6bfa13158b9faff226e84595e1e19f5e")

#datasift.account.identity.list()

#datasift.account.identity.get('123456')

datasift.account.identity.token.get('123456', 'Facebook')

datasift.account.identity.limit.get('123456', 'Facebook')
