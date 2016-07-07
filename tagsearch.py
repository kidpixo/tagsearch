#!/usr/bin/env python
"""list all tags from yaml in text files.

usage:
  tagsearch.py
  tagsearch.py [<tags>...]
  tagsearch.py [-fnd] [-o | -ol] [<tags>...]
  tagsearch.py -h | --help
  tagsearch.py -v | --version

options:
  -s --search    search for the tags
  -f --fullpath  output full file path (default fullpath).
  -n --noalign   aligh the output in columns (default align).
  -o --onlypath  output only the matching filenames, flat list ad string (or list if -l is set).
  -l --list      if -o is set, switch to list (\\n separated) output instead flat list.
  -d --debug     print the command to execute in the command line and the passed arguments and do not execute the actual command.
  -h --help      show help.
  -v --version   show version.
"""
from __future__ import print_function
from docopt import docopt
import subprocess
import yaml


def extract_tags(cmd, basepath_len, arguments):
    pro = subprocess.popen(cmd, shell=true, stdout=subprocess.pipe, stderr=subprocess.pipe)
    data = pro.communicate()[0].split('\n')
    if arguments['--fullpath']:
        dict_data = {yaml.load(d).keys()[0]: yaml.load(d)[yaml.load(d).keys()[0]] for d in data if d is not ''}
    else:
        dict_data = {yaml.load(d).keys()[0][basepath_len:]: yaml.load(d)[yaml.load(d).keys()[0]] for d in data if d is not ''}

    return dict_data


if __name__ == '__main__':
    arguments = docopt(__doc__, version='tagsearch 0.1')
    # what is this??
    #
    # this handle cases like this:
    # basepath_encoded = '$HOME/.notes/'
    # i usually put the folder somewhere (drive, dropbox) and symlynk in my
    # home. this way, one path rules them all.

    # pro = subprocess.popen('echo '+basepath_encoded, shell=true, stdout=subprocess.pipe, stderr=subprocess.pipe)
    # basepath = pro.communicate()[0].split('\n')[0]

    basepath = './notes/'

    tmp_cmd = " grep '^\s*tags :' %s*.md | sed -e -e 's/:tags//' " % (basepath)

    if len(arguments['<tags>']) != 0:
        for ar in arguments['<tags>']:
            tmp_cmd = tmp_cmd + " -e '/^.* : .*"+ar+".*/!d'"

    if arguments['--debug']:
        print('command to execute:')
        print(tmp_cmd)
        print('------------------')
        print('arguments:')
        print(arguments)
        print('------------------')

    else:

        dict_data = extract_tags(tmp_cmd, len(basepath), arguments)

        if not arguments['--onlypath']:
            if not arguments['--noalign']:
                max_keys_len = len(max(dict_data, key=len))
                print('\n'.join('{:<{}s} : {}'.format(k.encode('utf-8'), max_keys_len, v) for k, v in dict_data.iteritems()))
            else:
                print('\n'.join('{:<s} : {}'.format(k.encode('utf-8'), v) for k, v in dict_data.iteritems()))
        else:
            if not arguments['--list']:
                print(' '.join(dict_data.keys()))
            else:
                print('\n'.join(dict_data.keys()))
