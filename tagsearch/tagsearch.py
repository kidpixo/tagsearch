"""list all tags from yaml in text files.

Witouht any paramter, list all the files and tags.
Tags with ! prepended are delete from result.

Basics:

  tagsearch.py foo !bar

search for all notes containing tag `foo` and exclude all with of `bar`,
repeat the tags at will.

Usage:
  tagsearch.py
  tagsearch.py [<tags>...]
  tagsearch.py [-faescd] [-p | -pl] [<tags>...]
  tagsearch.py -h | --help
  tagsearch.py -v | --version

Options:
  -f --fullpath     output full file path (default False).
  -a --align        aligh the output in columns (default False).
  -p --pathonly     output only the matching filenames
  -l --list         flat list output, requires -p|--pathhonly.
  -e --errorformat  output vim errorformat `%f:%l:%m` for quickfix, implies -f|--fullpath.
  -s --escape       escape the filenames with " to protect whitespaces
  -c --check        check if all data contains frontmatter and, a 'tags' entry, if tags is a list, TODO
  -d --debug        print the command to execute in the command line and the passed arguments and do not execute the actual command.
  -h --help         show help.
  -v --version      show version.
"""
import pathlib
import subprocess
from docopt import docopt


def data_base_path_checker(default_data_path=None):
    """ data_base_path_checker checks if the default base_path is in shell
    enviroment variable $TAGSEARCH_HOME, if not fall back to standard ~/.notes.

    default_base is for testing purpose, if passed the function returns it.

    Path could be in the contracted + absolute form:

       ~/.notes

    If not starting with `/` it will be considered relative to cwd:
        
        notes > expand to $(pwd)/notes

    NOTE :  $HOME/.notes is not implemented.
    """

    if default_data_path :
        return pathlib.Path(default_data_path).expanduser().absolute()
    else :
        import os
        default_data_path = os.getenv('TAGSEARCH_HOME')
        if not default_data_path :
            default_data_path = '~/.notes'
        return pathlib.Path(default_data_path).expanduser().absolute()

def load_data_to_tinydb(data_base_path):
    """load_data_to_tinydb : parse the input directory and load the 
    frontmatter in the tinydb, skip file without tag.

    Parameters
    ----------

    data_base_path : pathlib.Path to data location

    Returns
    -------

    db : tinydb.TinyDB with data loaded in

    """
    import tinydb as tdb
    import frontmatter

    # the quickest implementation, see extra data
    metadatas = []
    db = tdb.TinyDB(storage=tdb.storages.MemoryStorage)
    for file in data_base_path.rglob('*md'):
        with file.open() as f:
            metadata, content = frontmatter.parse(f.read())
            if 'tags' in metadata:
                if len(metadata['tags']) == 0:
                   metadata['tags'] = ['']
                metadata['file'] = file
                metadatas.append(metadata)
    tmp = db.insert_multiple(metadatas)
    return db


def query_db(arg_tags,db):
    """query_db

    Parameters
    ----------
    arg_tags : list of tags
    db : tinydb.TinyDB instance loaded with data

    Returns
    -------

    list : result of query on db

    """
    # this is far more quick for empty input, just return everything
    if arg_tags:
        import tinydb as tdb
        from itertools import groupby
        # 1. split tags in include, exclude
        # 2. sort the tags based on first character
        # 3. use itertools to split args
        strip_exclamation = lambda s : s[1:] if s.startswith('!') else s
        keys={1:'exclude',0:'include'}
        arg_tags_split = {keys[k]:list(map(strip_exclamation,g)) for k,g in groupby( sorted(arg_tags, key=lambda i:i[0]), lambda i: i[0] == '!')}
        # all include tag in document - any of exclude tags

        if ('exclude' in arg_tags_split) & ('include' in arg_tags_split):
            return db.search(tdb.Query().tags.all(arg_tags_split['include']) & ~tdb.Query().tags.any(arg_tags_split['exclude']))
        elif ('include' in arg_tags_split):
            return db.search(tdb.Query().tags.all(arg_tags_split['include']))
        elif ('exclude' in arg_tags_split):
            return db.search(~tdb.Query().tags.any(arg_tags_split['exclude']))
    else:
        return db.all()


def print_results(arguments, result):
    """print_results

    Parameters
    ----------
    argument : dict of command line arguments
    result : list, result of tinydb query

    Returns
    -------
    None

    """
   
    show_path = lambda p: str(p) if arguments['--fullpath'] else p.name

    escape_char = '"' if arguments['--escape'] else '' 

    if arguments['--pathonly']:
        rows_sep = ' ' if arguments['--list'] else '\n' # this happens only if pathonly is set
        print(rows_sep.join(['{esc}{path}{esc}'.format(esc=escape_char,path=show_path(row['file'])) for row in result]))
        return 0

    if arguments['--errorformat']:
        print('\n'.join(['{path}:1:{tags}'.format(path=show_path(row['file']),tags=row['tags']) for row in result]))
        return 0
    
    # this happens if nothing else 
    max_file_field = max((len(show_path(row['file'])) for row in result)) if arguments['--align'] else 0

    print('\n'.join(['{path:<{max}}:{tags}'.format(max=max_file_field, path=show_path(row['file']),tags=row['tags']) for row in result]))
    return 0

if __name__ == '__main__':

    # process : parse args
    #   input : docopt default is argument vector passed to your program  (sys.argv[1:])
    #  output : dict 
    arguments = docopt(__doc__, version='tagsearch 0.1')

    # process: check data location
    # TODO   : add option to pass location in arguments? 
    #  input : ENVIROMENT var/config
    # output : pathlib.Path 
    data_base_path = data_base_path_checker()
    # 29.7 µs ± 494 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

    # process: load data and build in memory tinydb
    # TODO   : 
    #  input : data location, pathlib.Path
    # output : tinydb.TinyDB
    db = load_data_to_tinydb(data_base_path) 
    # 1000 files : 620 ms ± 63.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    # process: query the data
    #  input : tags lists, data db 
    # output : list of output
    result = query_db(arguments['<tags>'], db)

    if arguments['--debug'] :
        import pprint
        print(data_base_path)
        pprint.pprint(arguments)

    # process: data output 
    #  input : result of query + parsed user option 
    # output : print formatted results
    print_results(arguments, result)


# # get all uniques tags
# import itertools
# all_tags = set(itertools.chain(*[row['tags'] for row in result if 'tags' in row]))
# all_tags.discard('')
