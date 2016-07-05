#!/usr/bin/env python
"""List all tags from yaml in text files.

Usage:
  alltags.py
  alltags.py <tags>...
  alltags.py -h | --help
  alltags.py -v | --version
  alltags.py [-fn] [-o | -ol] [<tags>...]

Options:
  -h --help      show help.
  -v --version   show version.
  -f --fullpath  output full file path (default fullpath).
  -n --noalign   aligh the output in columns (default align).
  -o --onlypath  output only the matching filenames, flat list ad string (or list if -l is set).
  -l --list      if -o is set, switch to list (\\n separated) output instead flat list.
"""
from docopt import docopt
import subprocess


def extract_tags(cmd, basepath_len, arguments):
    import yaml
    pro = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = pro.communicate()[0].split('\n')
    if arguments['--fullpath']:
        dict_data = {yaml.load(d).keys()[0]: yaml.load(d)[yaml.load(d).keys()[0]] for d in data if d is not ''}
    else:
        dict_data = {yaml.load(d).keys()[0][basepath_len:]: yaml.load(d)[yaml.load(d).keys()[0]] for d in data if d is not ''}

    return dict_data


if __name__ == '__main__':
    arguments = docopt(__doc__, version='alltags 0.1')
    basepath_encoded = './notes/'
    pro = subprocess.Popen('echo '+basepath_encoded, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    basepath = pro.communicate()[0].split('\n')[0]

    tmp_cmd = " grep '^tags :' "+basepath+"*.md | sed -E -e 's/:tags//' "

    if len(arguments['<tags>']) != 0:
        for ar in arguments['<tags>']:
            tmp_cmd = tmp_cmd + " -e '/^.* : .*"+ar+".*/!d'"

    dict_data = extract_tags(tmp_cmd, len(basepath), arguments)

    if not arguments['--onlypath']:
        if not arguments['--noalign']:
            max_keys_len = max([len(k) for k, v in dict_data.iteritems()])
            print '\n'.join('{:<{}s} : {}'.format(k.encode('utf-8'), max_keys_len, v) for k, v in dict_data.iteritems())
        else:
            print '\n'.join('{:<s} : {}'.format(k.encode('utf-8'), v) for k, v in dict_data.iteritems())
    else:
        if not arguments['--list']:
            print ','.join(dict_data.keys())
        else:
            print '\n'.join(dict_data.keys())
    # print(arguments)
