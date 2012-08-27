# encoding: utf-8

import sys, os
from datetime import datetime
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), "..", ".."),]
import datasift
from env import Env

def usage(message = '', exit = True):
    """
    Display usage information, with an error message if provided.
    """
    if len(message) > 0:
        sys.stderr.write('\n%s\n' % message)
    sys.stderr.write('\n');
    sys.stderr.write('Usage: push-stream-from-csdl.py <username> <api_key> \\\n')
    sys.stderr.write('             <output_type> <hash_type> <hash> <name> ...\n')
    sys.stderr.write('\n')

    sys.stderr.write('Where: csdl_filename = a file containing the CSDL\n')
    sys.stderr.write('       start_date    = historic query start date (yyyymmddhhmmss)\n')
    sys.stderr.write('       end_date      = historic query end date (yyyymmddhhmmss)\n')
    sys.stderr.write('       sources       = comma separated list of sources (twitter,digg,etc)\n')
    sys.stderr.write('       sample        = percentage of matches to return\n')
    sys.stderr.write('       output_type   = http (currently only http is supported)\n')
    sys.stderr.write('       name          = a friendly name for the subscription\n')
    sys.stderr.write('       key=val       = output_type-specific arguments\n')
    sys.stderr.write('\n')
    sys.stderr.write('Example\n')
    sys.stderr.write('       push-stream-from-csdl.py csdl.txt 20120701000000 20120701235959 twitter 1 http \\\n')
    sys.stderr.write('               PushName delivery_frequency=10 url=http://www.example.com/push_endpoint \\\n')
    sys.stderr.write('               auth.type=none\n')
    sys.stderr.write('\n')
    if exit:
        sys.exit(1)

# Set up the environment
env = Env(sys.argv)

# Make sure we have enough arguments
if env.get_arg_count() < 7:
    usage()

# Get the args
csdl_filename = env.get_arg(0)
start_date    = env.get_arg(1)
end_date      = env.get_arg(2)
sources       = env.get_arg(3)
sample        = env.get_arg(4)
output_type   = env.get_arg(5)
name          = env.get_arg(6)

# Parse the dates from the command line
in_format  = '%Y%m%d%H%M%S'
out_format = '%s'
start      = datetime.strptime(start_date, in_format).strftime(out_format)
end        = datetime.strptime(end_date,   in_format).strftime(out_format)

# Read the CSDL file
csdl = open(csdl_filename, 'r').read()

try:
    # Create the stream definition
    streamdef = env.get_user().create_definition(csdl)

    # Create the historic
    historic = streamdef.create_historic(start, end, sources.split(','), sample, '%s_historic' % (name))

    # Display the details of the Historics query
    print 'Historics query:'
    env.display_historic_details(historic)
    print ''

    # Create the Push definition
    pushdef = env.get_user().create_push_definition()
    pushdef.set_output_type(output_type)

    # Now add the output_type-specific args from the command line
    for arg in env.get_args()[7:]:
        key, val = arg.split('=')
        pushdef.set_output_param(key, val)

    # Subscribe the historic to the hash
    sub = pushdef.subscribe_historic(historic, name)

    # Start the Historics query
    historic.start()

    # Display the details of the new subscription
    print 'Push subscription:'
    env.display_subscription_details(sub)
except datasift.InvalidDataError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)
except datasift.APIError, e:
    sys.stderr.write('APIError: %s\n' % e)
except datasift.AccessDeniedError, e:
    sys.stderr.write('AccessDeniedError: %s\n' % e)

sys.stderr.write('Rate-limit-remaining: %s\n' % str(env.get_user().get_rate_limit_remaining()));
