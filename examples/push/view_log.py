# encoding: utf-8

# This example displays the log for all or one subscription in your account.

import sys, os
from datetime import datetime
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), "..", ".."),]
import datasift
from env import Env

# Set up the environment
env = Env(sys.argv)

# Do we have a subscription ID?
try:
    arg_count = env.get_arg_count()
    if arg_count > 1:
        sys.stderr.write('Please specify no more than one subscription ID\n')
        sys.exit(1)
    elif arg_count == 0:
        log = env.get_user().get_push_subscription_log()
    else:
        # Get the subscription ID
        subscription_id = env.get_arg(0)

        # Get the subscription
        log = env.get_user().get_push_subscription_log(subscription_id)

    # Display the log
    if log['count'] == 0:
        print 'No log entries found.'
    else:
        for log_entry in log['log_entries']:
            print datetime(log_entry['request_time']).strprint('%Y-%m-%d %H:%M:%S'),
            if env.get_arg_count() == 1:
                print '[%s]' % (log_entry['subscription_id']),
            success = ''
            if log_entry['success']:
                success = 'Success '
            print '%s%s' % (success, log_entry['message'])
except datasift.InvalidDataError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)
except datasift.APIError, e:
    sys.stderr.write('APIError: %s\n' % e)
except datasift.AccessDeniedError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)

sys.stderr.write('Rate-limit-remaining: %s\n' % str(env.get_user().get_rate_limit_remaining()));
