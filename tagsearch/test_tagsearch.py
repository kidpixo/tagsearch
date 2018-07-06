#!/usr/bin/env python
# vim: filetype=python tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-
# run interactive development enviroment without pycache:
# PYTHONDONTWRITEBYTECODE=1 jupyter-console-3.4 --kernel tagsearch

# basic loading for testing purpose
import tagsearch
import pathlib

def test_data_base_path_checker():
    # tagsearch function
    data_base_path = tagsearch.functions.data_base_path_checker('notes')
    # expected value
    cr = pathlib.Path()

    assert data_base_path == cr.absolute() / 'notes'

def test_load_data_to_tinydb():
    # tagsearch function
    #TODO relative to install dir : does it work for zipped/eggs/wheels?
    data_base_path = pathlib.Path(tagsearch.__file__).parent / 'notes'
    db = tagsearch.functions.load_data_to_tinydb(data_base_path)
    # expected value
    result_all = [{'tags': [''],
                  'file': data_base_path / 'notes 2.md'},
                 {'tags': ['foo'],
                  'file': data_base_path /'notes 3.md'},
                 {'tags': ['test', 'dog', 'bar', 'fish', '42'],
                  'file': data_base_path /'notes 4.md'},
                 {'tags': ['foo', 'spam', 'bar', 'test'],
                  'file': data_base_path /'notes 5.md'}]
    assert db.all() == result_all

def test_query_db():
    # tagsearch function
    #TODO relative to install dir : does it work for zipped/eggs/wheels?
    data_base_path = pathlib.Path(tagsearch.__file__).parent / 'notes'
    db = tagsearch.functions.load_data_to_tinydb(data_base_path)

# result = tagsearch.functions.query_db(arguments['<tags>'], db)

def test_print_results():
    pass
# tagsearch.functions.print_results(arguments, result)
 
