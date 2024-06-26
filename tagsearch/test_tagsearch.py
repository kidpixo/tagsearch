#!/usr/bin/env python
# vim: filetype=python tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-
# run interactive development enviroment without pycache:
# PYTHONDONTWRITEBYTECODE=1 jupyter-console-3.4 --kernel tagsearch

# basic loading for testing purpose
import tagsearch
import pathlib
import pytest

# some common data
data_base_path = pathlib.Path(tagsearch.__file__).parent / 'notes'
# those are values stroed in the db
result_all = [
             {'tags': ['nofrontmatter']                   , 'file': data_base_path / 'notes 0.md'},
             {'tags': ['notagskey']                       , 'file': data_base_path / 'notes 1.md', 'test': 'this is anoter key'},
             {'tags': ['tagsempty']                       , 'file': data_base_path / 'notes 2.md'},
             {'tags': ['foo']                             , 'file': data_base_path /'notes 3.md'},
             {'tags': ['test', 'dog', 'bar', 'fish', '42'], 'file': data_base_path /'notes 4.md'},
             {'tags': ['foo', 'spam', 'bar', 'test']      , 'file': data_base_path /'notes 5.md'}]

@pytest.mark.data_path
def test_data_base_path_default():
    """test base path for data from default"""
    # tagsearch function
    data_base_path = tagsearch.functions.data_base_path_checker()

    # expected value
    expected = pathlib.Path.home() / '.notes'

    assert data_base_path == expected

@pytest.mark.data_path
def test_data_base_path_os_environ_checker():
    """test base path for data from passed Environment Variable"""
    # expected value
    expected = pathlib.Path()

    # tagsearch function
    import os
    os.environ['TAGSEARCH_HOME'] = str(expected / 'notes')
    data_base_path = tagsearch.functions.data_base_path_checker()

    assert data_base_path == expected.absolute() / 'notes'

@pytest.mark.data_path
def test_data_base_path_checker():
    """test base path for data from passed value"""
    # tagsearch function
    data_base_path = tagsearch.functions.data_base_path_checker('notes')
    # expected value
    expected = pathlib.Path()

    assert data_base_path == expected.absolute() / 'notes'

def test_load_data_to_tinydb():
    # tagsearch function
    #TODO relative to install dir : does it work for zipped/eggs/wheels?
    db = tagsearch.functions.load_data_to_tinydb(data_base_path)
    # expected value

    assert db.all() == result_all

@pytest.mark.parametrize("tags,param_result", [
    ([''],None),
    ([],result_all),
    (['foo','42'],[]),
    (['foo','bar'],[result_all[5]]),
    pytest.param( ['foo','bar'],[result_all[0]], marks=pytest.mark.xfail),
    (['foo','!bar'],[ result_all[3]]),
    (['!foo','!bar'], result_all[0:3]),
    ],ids=['empty string',
           'no input',
           'two tags include no result',
           'two tags include with result',
           'two tags include with wrong result',
           '1 tag include/ 1 exclude with result',
           'two tags exclude with result',
])
def test_query_db(tags,param_result):
    # tagsearch function
    #TODO relative to install dir : does it work for zipped/eggs/wheels?
    data_base_path = pathlib.Path(tagsearch.__file__).parent / 'notes'
    db = tagsearch.functions.load_data_to_tinydb(data_base_path)
    result = tagsearch.functions.query_db(tags, db)
    
    # expected value from parametrize
    assert result == param_result

@pytest.mark.parametrize(
            'arguments, expected ',[
( {'--tagsonly': True},['dog','notagskey','tagsempty','nofrontmatter','foo','bar','fish','42','test','spam']),
( {'--pathonly': True},['notes 0.md', 'notes 1.md', 'notes 2.md', 'notes 3.md', 'notes 4.md', 'notes 5.md']),
( {'--errorformat': True},
    [ "notes 0.md:1:['nofrontmatter']",
        "notes 1.md:1:['notagskey']",
        "notes 2.md:1:['tagsempty']",
        "notes 3.md:1:['foo']",
        "notes 4.md:1:['test', 'dog', 'bar', 'fish', '42']",
        "notes 5.md:1:['foo', 'spam', 'bar', 'test']",
        ]),
( {'': True},
    [ "notes 0.md:['nofrontmatter']",
        "notes 1.md:['notagskey']",
        "notes 2.md:['tagsempty']",
        "notes 3.md:['foo']",
        "notes 4.md:['test', 'dog', 'bar', 'fish', '42']",
        "notes 5.md:['foo', 'spam', 'bar', 'test']",
        ]),
], ids= ['arg:tagsonly',
        'arg:pathonly',
        'arg:errorformat',
        'arg:default no arg',
    ])
@pytest.mark.output
def test_print_results(capsys, arguments, expected):
    # tagsearch function
    #TODO relative to install dir : does it work for zipped/eggs/wheels?
    data_base_path = pathlib.Path(tagsearch.__file__).parent / 'notes'
    db = tagsearch.functions.load_data_to_tinydb(data_base_path)
    printout = tagsearch.functions.print_results(arguments, result_all)
    
    out, err = capsys.readouterr()
    out = out.split('\n')
    out.remove('')

    assert sorted(expected) == sorted(out)
