#!/usr/bin/env python
# see [grep -r in python - Stack # Overflow](http://stackoverflow.com/questions/1863236/grep-r-in-python/1864383#1864383)
from __future__ import print_function
import glob
import re
import sys
import yaml


def file_yaml_extract(fname, yaml_header_max=1, verbose=False, debug=False):
    """
    Output the  lines in a file in the yaml header (front matter),
    stopping after yaml_header_max blocks (default 1).
    """
    yaml_delimiter_re = re.compile('---\n')
    yaml_header_max = yaml_header_max
    yaml_header_count = 0
    inside_yaml = 0
    outstring = u''
    try:
        with open(fname, "rt") as f:
            if verbose:
                print("i, inside_yaml, yaml_header_count,  yaml_header_max, line")
                print(-1, inside_yaml, yaml_header_count,  yaml_header_max, 'line', end='', sep=' :  ')
            for i, line in enumerate(f):
                if debug:
                    import ipdb
                    ipdb.set_trace()
                if yaml_header_count <= yaml_header_max:
                    if inside_yaml and not yaml_delimiter_re.search(line):
                        if verbose:
                            print(i, inside_yaml, yaml_header_count,  yaml_header_max, line, end='', sep=' :  ')
                        else:
                            outstring += line
                    else:
                        inside_yaml = 1 if not inside_yaml else 0
                        yaml_header_count += 1
                        if verbose:
                            print(i, inside_yaml, yaml_header_count,  yaml_header_max, line, end='', sep=' :  ')
                else:
                    return outstring
    except IOError:
        return ''


def file_match(fname, pat, yaml_header_max=1):
    """
    Output the matching lines in a file in the yaml header,
    stopping after yaml_header_max blocks (default 1).
    """
    yaml_delimiter_re = re.compile('---')
    yaml_header_max = 2*yaml_header_max
    inside_yaml = 0
    try:
        with open(fname, "rt") as f:
            for i, line in enumerate(f):
                inside_yaml += 1 if yaml_delimiter_re.search(line) else 0
                if pat.search(line) and inside_yaml <= yaml_header_max and not yaml_delimiter_re.search(line):
                    # print(i, inside_yaml, pat.search(line), line, end='', sep=' :  ')
                    print(line.strip('\n'))
    except IOError:
        return


def grep(dir_name):
    for filename in glob.glob(dir_name):
        # yaml_front_matter = file_yaml_extract(filename)
        # if yaml_front_matter is not '':
            # print(filename, yaml.load(yaml_front_matter))
        print(filename, [d for d in yaml.load_all(open(filename, 'r'))])

if len(sys.argv) != 2:
    u = "Usage: greppy.py <dir_name>\n"
    sys.stderr.write(u)
    sys.exit(1)

grep(sys.argv[1])
