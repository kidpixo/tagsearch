"== Tagsearch 
" path to the tagsearch.py script
let g:tagsearchcmd = "~/supersectrepath/tagsearch.py"
function Tagsearch(...)
    cgete system(g:tagsearchcmd . " -ef " . join(a:000,' '))  " populate quickfix and don't jump
    cw " show quickfix window
endfunction

" define a command to humanize function call
command!  -nargs=* Tagsearch call Tagsearch(<f-args>)

" function called as:
" :Tagsearch foo bar
