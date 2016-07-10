"== Tagsearch 
" path to the script
let g:tagsearchcmd = "~/Downloads/github_cloned/tagsearch/tagsearch.py"

function Tagsearch(...)
    "echom system(g:tagsearchcmd . " -enf  ". a:1)
    " populate the quickfix and don't jump at the first error
    cgete system(g:tagsearchcmd . " -enf  ". a:1)
    cw " show quickfix window already
endfunction

" function called as:
" :call Tagsearch("foo bar")
