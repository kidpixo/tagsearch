"== Tagsearch 
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

"" function called as:
" :Tagsearch foo bar
"" use completion for tags:
" :Tagsearch f<Tab>

