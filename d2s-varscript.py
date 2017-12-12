#!/usr/bin/env python

import json
import subprocess
import sys
from os import listdir, getcwd
from re import search
from agavepy.actors import get_context, get_client

def get_vars_env(agave_context):
    '''Checks that MSG, system, and outdir are present as
    context variables and returns their values'''
    required_keyset = set(['message_dict', 'system', 'outdir'])
    keyset = set(dict(agave_context).keys())
    assert required_keyset.issubset(keyset), 'Context is missing required keys (MSG, system, outdir): {}'.format(dict(agave_context).keys())
    return [ agave_context[x] for x in required_keyset ]

def get_vars_json(agave_context):
    '''Checks that container, system, and outdir are present
    in message_dict and returns their values'''
    mdict = context.message_dict
    required_keyset = set(['container', 'system', 'outdir'])
    keyset = set(mdict.keys())
    assert required_keyset.issubset(keyset), 'Context is missing required keys (MSG, system, outdir): {}'.format(mdict.keys())
    return [ mdict[x] for x in required_keyset ]

def get_vars(agave_context):
    '''Returns container, system, and outdir variables'''
    # check if passed as JSON
    if type(context.message_dict) is dict:
        c, s, o = get_vars_json(agave_context)
    else:
        c, s, o = get_vars_env(agave_context)
    return (c, s, o)

if __name__ == '__main__':

    # get context and client
    context = get_context()
    ag = get_client()

    # container, agave system, and path to outdir 
    container, system, outdir = get_vars(context)

    # execute d2s with bash
    print 'RUNNING CONTAINER', container
    bashcmd = 'bash /docker2singularity.sh {}'.format(container)
    process = subprocess.Popen(bashcmd.split()).wait()
    assert int(process) == 0, 'Command finished with non-zero status: '+str(process)

    # find image file produced
    print '\nFINDING IMG FILE'
    files = ' '.join(listdir('/output'))
    regex = container.replace('/', '_').replace(':', '_') + '-[0-9]{4}-[0-9]{2}-[0-9]{2}-\w{12}\.img'

    img_search = search(regex, files)
    assert img_search is not None, 'Image for container '+container+' not found in files: '+files

    img = '/output/'+str(img_search.group(0))
    print img

    # DEBUGGING
    print '\nDEBUGGING'
    debugcmds = [ 'date', 'df -h', 'docker ps', 'docker images' ]
    output = ''
    for i in debugcmds:
        p = subprocess.Popen(i.split(), stdout=subprocess.PIPE)
        output = output+'\n'+p.stdout.read()
    print output

    debugfile = str(container)+'_diagnostics.txt'
    with open(debugfile, 'w') as f:
        f.write(output)
    movecmd = 'mv '+debugfile+' /work/03761/jturcino/projects/docker/abaco-biocontainers/'
    process = subprocess.Popen(movecmd.split()).wait()
    assert int(process) == 0, 'Move command finished with non-zero status: '+str(process)

    # upload img to desired system with agavepy
    print '\nUPLOADING FILE'
    print 'System ID: {}'.format(system)
    print 'Path: {}'.format(outdir)
    file_upload = ag.files.importData(systemId = system,
                                      filePath = outdir,
                                      fileToUpload = open(img))

    print '\nPROCESS COMPLETE'
