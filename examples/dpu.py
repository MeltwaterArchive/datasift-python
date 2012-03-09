# encoding: utf-8

# This example gets the DPU associated with the stream given on the command
# line or piped/typed into STDIN. It  presents it in a nice ASCII table.]
# Note that the CSDL must be enclosed in quotes if given on the command line.
#
# python dpu.py 'interaction.content contains "football"'
#  or
# cat football.csdl | python dpu.py
#
# NB: Most of the error handling (exception catching) has been removed for
# the sake of simplicity. Nearly everything in this library may throw
# exceptions, and production code should catch them. See the documentation
# for full details.

import sys, os
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]
import config, datasift

# Let's get our CSDL from the command line, otherwise from stdin
if len(sys.argv) == 2:
	csdl = sys.argv[1]
else:
	csdl = ''.join(sys.stdin.readlines()).strip()

# Make sure we got something
if len(csdl) == 0:
	print 'CSDL is empty'
	print
	sys.exit(1)

# Create the User object
print 'Creating user...'
user = datasift.User(config.username, config.api_key)

# Create the definition object
print 'Creating definition...'
definition = user.create_definition(csdl)

# Get the DPU. This will compile the defintiion, so we catch potential errors
# from that.
print 'Getting DPU...'
try:
	dpu = definition.get_dpu_breakdown()
except CompileFailed, exception:
	print 'CSDL compilation failed: %s' % (exception)
	sys.exit(1)

# Format the DPU details for output in a table
dputable = []
maxlength = { 'target': len('Target'), 'times used': len('Times used'), 'complexity': len('Complexity') }
for tgt in dpu['detail']:
	dpu['detail'][tgt]['count'] = '%d' % dpu['detail'][tgt]['count']
	dpu['detail'][tgt]['dpu'] = '%.2f' % dpu['detail'][tgt]['dpu']

	maxlength['target'] = max(maxlength['target'], len(tgt))
	maxlength['times used'] = max(maxlength['times used'], len(dpu['detail'][tgt]['count']))
	maxlength['complexity'] = max(maxlength['complexity'], len(dpu['detail'][tgt]['dpu']))

	dputable.append({
		'target':     tgt,
		'times used': dpu['detail'][tgt]['count'],
		'complexity': dpu['detail'][tgt]['dpu'],
	})

	for tgt2 in dpu['detail'][tgt]['targets']:
		dpu['detail'][tgt]['targets'][tgt2]['count'] = '%d' % dpu['detail'][tgt]['targets'][tgt2]['count']
		dpu['detail'][tgt]['targets'][tgt2]['dpu'] = '%.2f' % dpu['detail'][tgt]['targets'][tgt2]['dpu']

		maxlength['target'] = max(maxlength['target'], 2 + len(tgt2))
		maxlength['times used'] = max(maxlength['times used'], len(dpu['detail'][tgt]['targets'][tgt2]['count']))
		maxlength['complexity'] = max(maxlength['complexity'], len(dpu['detail'][tgt]['targets'][tgt2]['dpu']))

		dputable.append({
			'target':     '  %s' % tgt2,
			'times used': dpu['detail'][tgt]['targets'][tgt2]['count'],
			'complexity': dpu['detail'][tgt]['targets'][tgt2]['dpu'],
		})

maxlength['complexity'] = max(maxlength['complexity'], len('%3.2f' % dpu['dpu']))

print
print '/-' + ('-' * (maxlength['target'] + maxlength['times used'] + maxlength['complexity'] + 6)) + '-\\'
print '| ' + 'Target'.ljust(maxlength['target']) + ' | ' + 'Times Used'.ljust(maxlength['times used']) + ' | ' + 'Complexity'.ljust(maxlength['complexity']) + ' |'
print '|-' + ('-' * maxlength['target']) + '-+-' + ('-' * maxlength['times used']) + '-+-' + ('-' * maxlength['complexity']) + '-|'
for row in dputable:
    print '| ' + row['target'].ljust(maxlength['target']) + ' | ' + row['times used'].rjust(maxlength['times used']) + ' | ' + row['complexity'].rjust(maxlength['complexity']) + ' |'
print '|-' + ('-' * (maxlength['target'] + maxlength['times used'] + maxlength['complexity'] + 6)) + '-|'
print '| ' + 'Total'.rjust(maxlength['target'] + 3 + maxlength['times used']) + ' = ' + ('%.2f' % dpu['dpu']).rjust(maxlength['complexity']) + ' |'
print '\\-' + ('-' * (maxlength['target'] + maxlength['times used'] + maxlength['complexity'] + 6)) + '-/'
print