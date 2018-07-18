# Tagsearch.py

[TOC]

[comment]: # [TOC] generate the Table of Contents on Bitbucket in Markdown files.

This program searches among tags in yaml header in text files in a single directory.

### why you should use it

If you ever had to skim through hundreds of text files searching for a particular topic, this could help.

Have all metadata stored in a simple portable text file without any central db.

### why you should not use it

Have all metadata stored in a simple portable text file without any central db. (this is not a typo!)

The data are reconstructed on the fly at each call, on modern computers with a reasonable number of file it takes less than 1 second.

If you don't like it, probably this is not for you.

## Basic usage
[^top](#markdown-header-tagsearchpy)

    tagsearch foo !bar

    notes 5.md  : ['foo',  'Monty', 'spaces', 'test']
    notes 41.md : ['foo', 'spaces', 'test', 'spam']

Returns  all files containing tag `foo` and exclude all with of `bar`.

The files location is stored in the shell variable `TAGSEARCH_HOME` or the default is `$HOME/.notes/` .
You need (obviously) to have some file for the script to run.
If you havent, see below [Test Run](#markdown-header-test-run)

Without any parameter, `tagsearch` lists all the files and tags in long formt.

Tags with ! prepended are delete from result.

Some special tags are reserved for internal use:

- `nofrontmatter` : files without frontmatter (bad format)
- `notagskey` : files without `tags` key
- `tagsempty` : files with empty in `tags` array

You can of course use them, but this will interfere with the aim of theese tags.

## Example file
[^top](#markdown-header-tagsearchpy)

```markdown
---
tags : [test, Monty]
---

Here could be wahtever you want: I use markdown for my file,
but you are free to use your style.

Header format could be changed to other format with minimal effort 
to JSON or TOML.
```

### Test Run
[^top](#markdown-header-tagsearchpy)

For a test run, execute 

```bash
$ cd utilites/
$ python generate_random_notes.py

$ TAGSEARCH_HOME=$(pwd)/notes tagsearch foo bar
notes 18.md : ['foo', 'bar', 'dog', 'Monty', 'test']
notes 5.md  : ['foo', 'bar', 'Monty', 'spaces', 'test']
notes 41.md : ['foo', 'spaces', 'bar', 'test', 'spam']
notes 20.md : ['bar', '42', 'spaces', 'dog', 'foo']
```

this generates 50 random notes in the `notes/` subfolder, then search for all the notes with foo AND bar in the tags.
The notes are randomly generated, your result may vary.

## Tagsearch.vim
[^top](#markdown-header-tagsearchpy)

Add this in your .vimrc (or source tagsearch.vim) and set the path to the 
`tagsearch` script (use the output of `which tagsearch`) in `g:tagsearchcmd`.

```vim
" path to the tagsearch.py script
let g:tagsearchcmd = "~/supersectrepath/tagsearch"

" define vimscript wrapper
function Tagsearch(...)
    cgete system(g:tagsearchcmd . " -ef " . join(a:000,' '))  " populate quickfix and don't jump
    cw " show quickfix window
endfunction

" define a completion function
function! TagsearchComp(ArgLead, CmdLine, CursorPos)
    return filter(systemlist(g:tagsearchcmd . " -t "), 'v:val =~ a:ArgLead')
endfunction

" define a command to humanize function call
command!  -nargs=* -complete=customlist,TagsearchComp Tagsearch call Tagsearch(<f-args>)
```

This define the command `Tagsearch` and completion based on all your tags.

Usage:

    :Tagsearch foo [<Tab><Tab>]

This will :

- execute tagsearch.py wiht `-ef foo bar` as arguments
- optional Tab will present you all your tags.
- populate the quickfix window with the results without jumping
- open the quickfix windoww

Using the excellent [tpope/vim-unimpaired](https://github.com/tpope/vim-unimpaired) (pairs of handy bracket mappings) you could navigate the results with `]q` (:cnext) and `[q]` ( :cprevious ).

## Bash Completion

In `utilites/tagsearch_completion.bash` put a simple bash completion function.

Now is just completing all the existing tags in your file list.

Just source it in your .bashrc like `. tagsearch_completion.bash`

### Usage
[^top](#markdown-header-tagsearchpy)

    tagsearch.py
    tagsearch.py [<tags>...]
    tagsearch.py [-faescd] [-p | -pl] [<tags>...]
    tagsearch.py -h | --help
    tagsearch.py -v | --version

#### Options
[^top](#markdown-header-tagsearchpy)

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
