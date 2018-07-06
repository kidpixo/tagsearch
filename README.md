# Tagsearch.py

This script search across all tags in yaml header in text files in a directory, default is in ~/.notes/ .
The idea is to store metadata in a simple text file to edit it with the editor of your choice.

A workflow is to search for a tag(s) and pipe the resulting filelist in a text editor. 

Below a [vim-script](#tagsearch.vim) function example.

Without any parameter, list all the files and tags.

Tags with ! prepended are delete from result.

Some special tags are reserved for internal use:

- `nofrontmatter` : files without frontmatter 
- `notagskey` : files without `tags` key
- `tagsempty` : files with empty in `tags` array

You can of course use them, but this will interfere with the aim of theese tags:
search form ill formatted files, files without `tags` key or any tag.

### WARNING: 

For a test run, execute 

```bash
$ ./generate_random_notes.py

$ ./tagsearch.py foo bar
notes 18.md : ['foo', 'bar', 'dog', 'Monty', 'test']
notes 5.md  : ['foo', 'bar', 'Monty', 'spaces', 'test']
notes 41.md : ['foo', 'spaces', 'bar', 'test', 'spam']
notes 20.md : ['bar', '42', 'spaces', 'dog', 'foo']
```

this generates 50 random notes in the `notes/` subfolder, then search for all the notes with foo AND bar in the tags.
The notes are randomly generated, your result may vary.

To edit the matching files in vim, pipe the result in vim quickfix directly from shell (bash):

```bash
$ vim -q <(./tagsearch.py -e foo bar)
```

or use the  `Tagsearch` [command](#markdown-header-tagsearchvim) below directly in vim.

## Tagsearch.vim

Add this in your .vimrc (or source tagsearch.vim) and set the path to the script 

```vim
" path to the tagsearch.py script
let g:tagsearchcmd = "~/supersectrepath/tagsearch.py"
function Tagsearch(...)
    cgete system(g:tagsearchcmd . " -ef " . join(a:000,' '))  " populate quickfix and don't jump
    cw " show quickfix window
endfunction
" define a command to humanize function call
command!  -nargs=* Tagsearch call Tagsearch(<f-args>)
```

This define the command `Tagsearch` that could be called as

    :Tagsearch foo bar

This will execute tagsearch.py wiht `-e foo bar` as arguments and populate the 
quickfix window with the results without jumping to the first.

The it will open the quickfix window.

Using the excellent [tpope/vim-unimpaired](https://github.com/tpope/vim-unimpaired) (pairs of handy bracket mappings) you could navigate the results with `]q` (:cnext) and `[q]` ( :cprevious ).

## Example file

```markdown
---
tags : [test, Monty]
---

# Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet,  consectetur adipiscing elit. 
Fusce consequat suscipit auctor. Quisque accumsan ex in 
auctor dignissim. In id.

```

## Using it

This is the [docopt](http://docopt.org/) documentation from the main script
`tagsearch/tagsearch`

### Basics

    tagsearch foo !bar

Returns  all files containing tag `foo` and exclude all with of `bar`.

### Usage

    tagsearch.py
    tagsearch.py [<tags>...]
    tagsearch.py [-faescd] [-p | -pl] [<tags>...]
    tagsearch.py -h | --help
    tagsearch.py -v | --version

### Options

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
