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
    sys.stderr.write('Usage: create-from-csdl.py <username> <api_key> \\\n')
    sys.stderr.write('            <csdl_filename> <start_date> <end_date> <sources> <sample> <name>\n')
    sys.stderr.write('\n')
    sys.stderr.write('Where: csdl_fileanme = a file containing the CSDL\n')
    sys.stderr.write('       start_date    = Historics query start date (yyyymmddhhmmss)\n')
    sys.stderr.write('       end_date      = Historics query end date (yyyymmddhhmmss)\n')
    sys.stderr.write('       sources       = the data sources the Historics query should match\n')
    sys.stderr.write('       sample        = what percentage of the matching interactions are required\n')
    sys.stderr.write('       name          = a friendly name for the Historics query\n')
    sys.stderr.write('\n')
    sys.stderr.write('Example\n')
    sys.stderr.write('       create-from-csdl.py csdl.txt 20120801120000 20120801130000 twitter 100 \\\n')
    sys.stderr.write('                         MyHistoricsQuery\n')
    sys.stderr.write('\n')
    if exit:
        sys.exit(1)

# Set up the environment
env = Env(sys.argv)

# Make sure we have enough arguments
if env.get_arg_count() != 6:
    usage()

# Get the args
csdl_filename = env.get_arg(0)
start_date    = env.get_arg(1)
end_date      = env.get_arg(2)
sources       = env.get_arg(3)
sample        = env.get_arg(4)
name          = env.get_arg(5)

# Parse the dates from the command line
in_format  = '%Y%m%d%H%M%S'
out_format = '%s'
start      = datetime.strptime(start_date, in_format).strftime(out_format)
end        = datetime.strptime(end_date,   in_format).strftime(out_format)

try:
    # Create the Historics query
    historic = env.get_user().create_historic(stream_hash, start, end, sources.split(','), sample, name)

    # Display the details of the new Historics query
    env.display_historic_details(historic)
except datasift.InvalidDataError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)
except datasift.AccessDeniedError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)

sys.stderr.write('Rate-limit-remaining: %s\n' % str(env.get_user().get_rate_limit_remaining()));
