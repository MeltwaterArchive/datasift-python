# encoding: utf-8

# This example lists the current Historics queries in your account.

import sys, os
from datetime import datetime
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), "..", ".."),]
import datasift
from env import Env

# Set up the environment
env = Env(sys.argv)

try:
    # Get the list of Historics queries in your account
    queries = env.get_user().list_historics()

    if len(queries['historics']) == 0:
        print 'There are no Historics queries in your account.'
    else:
        # Display the details of each query in the response
        for historic in queries['historics']:
            env.display_historic_details(historic)
            print '--'
except datasift.InvalidDataError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)
except datasift.APIError, e:
    sys.stderr.write('APIError: %s\n' % e)
except datasift.AccessDeniedError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)

sys.stderr.write('Rate-limit-remaining: %s\n' % str(env.get_user().get_rate_limit_remaining()));
