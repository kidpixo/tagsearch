
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
    import pathlib

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
            if metadata: # frontamatter present
                if 'tags' in metadata: # tag key present in frontmatter
                    if len(metadata['tags']) == 0: # not values in tags
                       metadata['tags'] = ['tagsempty']
                else: # no tags key in frontmatter
                       metadata['tags'] = ['notagskey']
            else: # frontamatter nor tag key present
                metadata['tags'] = ['nofrontmatter']

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
    # this is far more quick for empty input or just one empty string, just return everything
    if len(arg_tags) == 1 and '' in arg_tags[0]:
        return None
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
    # this does nothing if None or epmty result list is passed
    if result: 

        show_path = lambda p: str(p) if arguments['--fullpath'] else p.name
        rows_sep = ' ' if arguments['--list'] else '\n' # this happens only if pathonly is set
        newline_char = '\n' if arguments['--list'] else ' '
        escape_char = '"' if arguments['--escape'] else ''

        if arguments['--pathonly']:
            print(rows_sep.join(['{esc}{path}{esc}'.format(esc=escape_char,path=show_path(row['file'])) for row in result]))
            return 0

        if arguments['--errorformat']:
            print(f'{rows_sep}'.join(['{path}:1:{tags}'.format(path=show_path(row['file']),tags=row['tags']) for row in result]))
            return 0
        
        # this happens if nothing else 
        max_file_field = max((len(show_path(row['file'])) for row in result)) if arguments['--align'] else 0

        if arguments['--tagsonly']:
            # get all uniques tags
            import itertools
            all_tags = set(itertools.chain(*[row['tags'] for row in result if 'tags' in row]))
            # 
            print(f'{rows_sep}'.join([f'{escape_char}{t}{escape_char}' if isinstance(t,str) else f'{escape_char}{str(t)}{escape_char}' for t in all_tags]))
            return 0

        print('\n'.join(['{path:<{max}}:{tags}'.format(max=max_file_field, path=show_path(row['file']),tags=row['tags']) for row in result]))
        return 0



