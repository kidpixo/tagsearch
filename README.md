# Tagsearch.py

The script lists all tags from yaml in text files.

Witouht any paramter, list all the files and tags.

Tags with ! prepended are delete from result.

WARNING: please, no `:` in filename , this mess up with the yaml format.

For a test run, execute 

    python generate_random_notes.py

this generates 50 random notes in the `notes/` subfolder.

Then use 

    ./tagsearch -h

for the documentation.

## Tagsearch.vim

in your .vimrc set the path to the script

```vim
let g:tagsearchcmd = "~/supersectrepath/tagsearch.py"
function Tagsearch(...)
    "echom system(g:tagsearchcmd . " -enf  ". a:1)
    " populate the quickfix and don't jump at the first error
    cgete system(g:tagsearchcmd . " -enf  ". a:1)
    cw " show quickfix window already
endfunction
```
This define the function Tagsearch tha could be called as:

    call Tagsearch("foo bar")

This will execute tagsearch.py wiht `"foo bar"` as arguments and populate the 
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
