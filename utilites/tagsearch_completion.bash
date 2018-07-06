_tagsearch_completions() {
COMPREPLY=($(compgen -W "$(tagsearch -t)" -- "${COMP_WORDS[-1]}"))
}

complete -F _tagsearch_completions tagsearch
