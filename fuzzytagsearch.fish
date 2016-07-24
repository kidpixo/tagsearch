function fuzzytagsearch
    # function for fish shell, the reeking fishy awesome shell.
    # fuzzy search in tags search result and open result in vim.
    # Requiresment and Assumptions:
    # - fzf installed and available in $PATH
    # - notes reside in ~/.notes/, change at your will.

    tagsearch $argv | fzf | cut -d":" -f 1 | xargs -I sel echo "$HOME/.notes/"sel | read -l fzf_local_result
    if test -e $fzf_local_result
        vim "$fzf_local_result"
    else
        echo "File does not exist $fzf_local_result"
    end
end
