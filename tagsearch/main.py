# -*- coding: utf-8 -*-
"""Search all tags from yaml frontmatter in text files.
Files location is in the TAGSEARCH_HOME variable or $HOME/.notes.
Witouht any paramter, list all the files and tags.
A !TAG exclude TAG from result.

Basics:

  tagsearch foo !bar

Returns  all files containing tag `foo` and exclude all with of `bar`.

Usage:
  tagsearch.py
  tagsearch.py [<tags>...]
  tagsearch.py [-faescd] [-p | -pl] [-t | -tl] [<tags>...]
  tagsearch.py -h | --help
  tagsearch.py -v | --version

Options:
  -f --fullpath     output full file path (default False).
  -a --align        aligh the output in columns (default False).
  -p --pathonly     output only the filenames
  -t --tagsonly     output only the unique tags
  -l --list         flat list output, requires -p|--pathhonly or -t|--tagsonly.
  -e --errorformat  output vim errorformat `%f:%l:%m` for quickfix, implies -f|--fullpath.
  -s --escape       escape the filenames with " to protect whitespaces
  -c --check        check if all data contains frontmatter and, a 'tags' entry, if tags is a list, TODO
  -d --debug        print the command to execute in the command line and the passed arguments and do not execute the actual command.
  -h --help         show help.
  -v --version      show version.
"""


def main():
    import tagsearch
    # process : parse args
    #   input : docopt default is argument vector passed to your program  (sys.argv[1:])
    #  output : dict 
    from docopt import docopt
    arguments = docopt(__doc__, version='tagsearch 0.1')

    # process: check data location
    # TODO   : add option to pass location in arguments? 
    #  input : ENVIROMENT var/config
    # output : pathlib.Path 
    data_base_path = tagsearch.functions.data_base_path_checker()
    # 29.7 µs ± 494 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

    # process: load data and build in memory tinydb
    # TODO   : 
    #  input : data location, pathlib.Path
    # output : tinydb.TinyDB
    db = tagsearch.functions.load_data_to_tinydb(data_base_path) 
    # 1000 files : 620 ms ± 63.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    # process: query the data
    #  input : tags lists, data db 
    # output : list of output
    result = tagsearch.functions.query_db(arguments['<tags>'], db)

    if arguments['--debug'] :
        import pprint
        print(data_base_path)
        pprint.pprint(arguments)

    # process: data output 
    #  input : result of query + parsed user option 
    # output : print formatted results
    tagsearch.functions.print_results(arguments, result)
