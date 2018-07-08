# Tagsearch.py

# Table Of Content

- [Test Run](#markdown-header-test-run)
- [Tagsearch.vim](#markdown-header-tagsearch.vim)
- [Example file](#markdown-header-example-file)
- [Use from Commandline](#markdown-header-use-from-commandline)
    - [Basics](#markdown-header-basics)
    - [Usage](#markdown-header-usage)
    - [Options](#markdown-header-options)


This script does one thing : search across all tags in yaml header in text files in
a directory.

The files location is stored in the shell variavle `TAGSEARCH_HOME` or the default 
is `$HOME/.notes/` .

The idea is to store metadata in a simple portable text file without any central db.

The only drawback is that the data are reconstructed on the fly at each call, but on
modern computer with a reasnoable number of file it takes less than 1 second.

Some informal benchmarks on my laptop shows ~1.5s with 10000 files, 
with a couple of hundreds the whole script runs in about ~0.5s.

## Example file
[^top](#markdown-header-tagsearchpy)

```markdown
---
tags : [test, Monty]
---

# Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet,  consectetur adipiscing elit. 
Fusce consequat suscipit auctor. Quisque accumsan ex in 
auctor dignissim. In id.

```

Below a [vim-script](#markdown-header-tagsearch.vim) function example.

Without any parameter, list all the files and tags.

Tags with ! prepended are delete from result.

Some special tags are reserved for internal use:

- `nofrontmatter` : files without frontmatter (bad format)
- `notagskey` : files without `tags` key
- `tagsempty` : files with empty in `tags` array

You can of course use them, but this will interfere with the aim of theese tags.

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

To edit the matching files in vim, pipe the result in vim quickfix directly from shell (bash):

```bash
$ vim -q <(./tagsearch.py -e foo bar)
```

or use the  `Tagsearch` [command](#markdown-header-tagsearchvim) below directly in vim.

## Tagsearch.vim
[^top](#markdown-header-tagsearchpy)

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

This will :

- execute tagsearch.py wiht `-ef foo bar` as arguments
- populate the quickfix window with the results without jumping
- open the quickfix windowi

Using the excellent [tpope/vim-unimpaired](https://github.com/tpope/vim-unimpaired) (pairs of handy bracket mappings) you could navigate the results with `]q` (:cnext) and `[q]` ( :cprevious ).

## Completion

In `utilites/tagsearch_completion.bash` put a simple bash completion function.

Now is just completing all the existing tags in your file list.

Just source it in your .bashrc like `. tagsearch_completion.bash`


## Use from Commandline
[^top](#markdown-header-tagsearchpy)

This is the [docopt](http://docopt.org/) documentation from the main script
`tagsearch/tagsearch`

### Basics
[^top](#markdown-header-tagsearchpy)

    tagsearch foo !bar

Returns  all files containing tag `foo` and exclude all with of `bar`.

### Usage
[^top](#markdown-header-tagsearchpy)

    tagsearch.py
    tagsearch.py [<tags>...]
    tagsearch.py [-faescd] [-p | -pl] [<tags>...]
    tagsearch.py -h | --help
    tagsearch.py -v | --version

### Options
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
