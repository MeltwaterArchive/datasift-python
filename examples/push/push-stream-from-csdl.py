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
    sys.stderr.write('       output_type   = http (currently only http is supported)\n')
    sys.stderr.write('       name          = a friendly name for the subscription\n')
    sys.stderr.write('       key=val       = output_type-specific arguments\n')
    sys.stderr.write('\n')
    sys.stderr.write('Example\n')
    sys.stderr.write('       PushFromHash csdl.txt http \"Push Name\" delivery_frequency=10 \\\n')
    sys.stderr.write('                    url=http://www.example.com/push_endpoint auth.type=none\n')
    sys.stderr.write('\n')

    sys.stderr.write('\n')
    if exit:
        sys.exit(1)

# Set up the environment
env = Env(sys.argv)

# Make sure we have enough arguments
if env.get_arg_count() < 3:
    usage()

# Get the args
csdl_filename = env.get_arg(0)
output_type   = env.get_arg(1)
name          = env.get_arg(2)

# Read the CSDL file
csdl = open(csdl_filename, 'r').read()

try:
    # Create the stream definition
    streamdef = env.get_user().create_definition(csdl)

    # Create the Push definition
    pushdef = env.get_user().create_push_definition()
    pushdef.set_output_type(output_type)

    # Now add the output_type-specific args from the command line
    for arg in env.get_args()[3:]:
        key, val = arg.split('=')
        pushdef.set_output_param(key, val)

    # Subscribe the definition to the hash
    sub = pushdef.subscribe_definition(streamdef, name)

    # Display the details of the new subscription
    env.display_subscription_details(sub)
except datasift.InvalidDataError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)
except datasift.APIError, e:
    sys.stderr.write('APIError: %s\n' % e)
except datasift.AccessDeniedError, e:
    sys.stderr.write('AccessDeniedError: %s\n' % e)

sys.stderr.write('Rate-limit-remaining: %s\n' % str(env.get_user().get_rate_limit_remaining()));
