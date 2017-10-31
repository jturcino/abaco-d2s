#!/usr/bin/env python

import json
import subprocess
import sys
from os import listdir, getcwd
from re import search
from agavepy.actors import get_context, get_client

if __name__ == '__main__':

    # get context and client
    context = get_context()
    ag = get_client()

    # get container, agave system, and path to outdir
    container = str(context['MSG']).replace("'", "")
    assert ' ' not in container, 'Spaces in container name: '+container

    system = str(context['system'])
    assert ' ' not in system, 'Spaces in system name: '+system

    outdir = str(context['outdir'])
    assert ' ' not in outdir, 'Spaces in outdir path: '+outdir

    print 'INITIAL FILES:\n  '+'\n  '.join(listdir('.'))

    # execute d2s with bash
    print '\nRUNNING CONTAINER'
    bashcmd = 'bash /docker2singularity.sh '+container
    process = subprocess.Popen(bashcmd.split()).wait()
    print 'Return code:', str(process)
    assert int(process) == 0, 'Command finished with non-zero status: '+str(process)

    # find image file produced
    print '\nOUTPUT FILES:\n  '+'\n  '.join(listdir('/output/'))
    files = ' '.join(listdir('/output'))
    regex = container.replace('/', '_').replace(':', '_') + '-[0-9]{4}-[0-9]{2}-[0-9]{2}-\w{12}\.img'
    print '\nREGEX:', regex

    img_search = search(regex, files)
    assert img_search is not None, 'Image for container '+container+' not found in files: '+files
    img = '/output/'+str(img_search.group(0))
    print '\n\nIMG:', img

    # upload img to desired system with agavepy
    file_upload = ag.files.importData(systemId = system,
                                      filePath = outdir,
                                      fileToUpload = open(img))
