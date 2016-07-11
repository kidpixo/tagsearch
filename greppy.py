#!/usr/bin/python
# see [grep -r in python - Stack # Overflow](http://stackoverflow.com/questions/1863236/grep-r-in-python/1864383#1864383)
import os
import re
import sys


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


def grep(dir_name, s_pat):
    pat = re.compile(s_pat)
    for dirpath, dirnames, filenames in os.walk(dir_name):
        for fname in filenames:
            fullname = os.path.join(dirpath, fname)
            file_match(fullname, pat)

if len(sys.argv) != 3:
    u = "Usage: pygrep <dir_name> <pattern>\n"
    sys.stderr.write(u)
    sys.exit(1)

grep(sys.argv[1], sys.argv[2])
