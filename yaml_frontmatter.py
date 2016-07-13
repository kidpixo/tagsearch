#!/usr/bin/python
# see [grep -r in python - Stack # Overflow](http://stackoverflow.com/questions/1863236/grep-r-in-python/1864383#1864383)
import os
import sys
import yaml


def grep(dir_name):
    for dirpath, dirnames, filenames in os.walk(dir_name):
        for fname in filenames:
            with open(os.path.join(dirpath, fname), 'r') as f:
                front_matter = next(yaml.load_all(f))
                print fname, ' > ', front_matter


if len(sys.argv) != 2:
    u = "Usage: pygrep <dir_name> \n"
    sys.stderr.write(u)
    sys.exit(1)

print sys.argv

grep(sys.argv[1])
