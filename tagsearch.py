#!/usr/bin/env python
"""list all tags from yaml in text files.

Witouht any paramter, list all the files and tags.
Tags with ! prepended are delete from result.

Usage:
  tagsearch.py
  tagsearch.py [<tags>...]
  tagsearch.py [-fnd] [-t | -tl] [-p | -pl] [<tags>...]
  tagsearch.py [-t | -p] [<tags>...]
  tagsearch.py -h | --help
  tagsearch.py -v | --version

Options:
  -f --fullpath  output full file path (default fullpath).
  -n --noalign   aligh the output in columns (default align).
  -p --pathonly  output only the matching filenames, flat list ad string (or list if -l is set).
  -t --tagonly   output only the tags of matching files.
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
    pro = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = pro.communicate()[0].split('\n')

    if not (len(data) == 1) or (bool(data[0])):
        if arguments['--fullpath']:
            dict_data = {yaml.load(d).keys()[0]: yaml.load(d)[yaml.load(d).keys()[0]] for d in data if d is not ''}
        else:
            dict_data = {yaml.load(d).keys()[0][basepath_len:]: yaml.load(d)[yaml.load(d).keys()[0]] for d in data if d is not ''}
    else:
        dict_data = {}

    return dict_data


if __name__ == '__main__':
    arguments = docopt(__doc__, version='tagsearch 0.1')
    # This handle cases like $HOME in the basepath.
    # I usually put the folder somewhere (drive, dropbox) and symlynk in my
    # home. This way, one path rules them all.
    # basepath_encoded = '$HOME/.notes/'
    # pro = subprocess.Popen('echo '+basepath_encoded, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # basepath = pro.communicate()[0].split('\n')[0]

    basepath = './notes/'

    tmp_cmd = " grep '^\s*tags :' %s*.md | sed -E -e 's/:tags//' " % (basepath)

    if len(arguments['<tags>']) != 0:
        tmp_cmd = tmp_cmd + ''.join([" -e '/^.* : .*"+ar[1:]+".*/d'" if ar[0] == "!" else " -e '/^.* : .*"+ar+".*/!d'" for ar in arguments['<tags>']])

    if arguments['--debug']:
        print('------------------')
        print('command to execute:', tmp_cmd)
        print('------------------')
        print('arguments:')
        print(arguments)
        print('------------------')

    else:

        dict_data = extract_tags(tmp_cmd, len(basepath), arguments)
        if len(dict_data) != 0:               # not results in output
            if not arguments['--pathonly']:       # only path == True
                if not arguments['--noalign']:    # noalign == True
                    max_keys_len = len(max(dict_data, key=len))
                    print('\n'.join('{:<{}s} : {}'.format(k.encode('utf-8'), max_keys_len, v) for k, v in dict_data.iteritems()))
                else:                             # noalign == True
                    print('\n'.join('{:<s} : {}'.format(k.encode('utf-8'), v) for k, v in dict_data.iteritems()))
            else:                                 # only path == False
                if not arguments['--list']:       # list == True
                    print(' '.join(dict_data.keys()))
                else:                             # list == False
                    print('\n'.join(dict_data.keys()))
