# Tagsearch.py

This script search across all tags in yaml header in text files in a directory, default is in ~/.notes/ .
The idea is to store metadata in a simple text file to edit it with the editor of your choice.

A workflow is to search for a tag(s) and pipe the resulting filelist in a text editor. 

Below a [vim-script](#tagsearch.vim) function example.

Without any parameter, list all the files and tags.

Tags with ! prepended are delete from result.

A technical note: the script is essentially a python wrapper around a grep+sed pipe and it work well only for one yaml block in the document and if there aren't line similar to yaml tags. 

### WARNING: 

1. please, no `:` in filename , this mess up with the yaml format.
2. the actual script relies on grep and sed, if this isn't availabe on your system you are out of luck. I'm planning a pure python solution, if benchmarks will be good.

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

```markdown|
---
tags : [test, Monty]
---

# Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet,  consectetur adipiscing elit. 
Fusce consequat suscipit auctor. Quisque accumsan ex in 
auctor dignissim. In id.

```

## Usage

- tagsearch.py
- tagsearch.py [<tags>...]
- tagsearch.py [-dfne] [-p | -pl] [<tags>...]
- tagsearch.py -h | --help
- tagsearch.py -v | --version

## Options

- **-f --fullpath**    : output full file path (default fullpath).
- **-n --noalign**     : aligh the output in columns (default align).
- **-p --pathonly**    : output only the matching filenames, flat list ad string (or list if -l is set).
- **-l --list**        : if -o is set, switch to list (\n separated) output instead flat list, requires -p.
- **-d --debug**       : print the command to execute in the command line and the passed arguments and do not execute the actual command.
- **-e --errorformat** : produce output compatible with vim errorformat for quickfix window, implies -f and -n.
- **-h --help**        : show help.
- **-v --version**     : show version.
