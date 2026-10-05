# ============================================================
# PROMPT
# ============================================================

git_prompt() {
    local branch status ahead behind

    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        GIT_PROMPT=""
        return
    fi

    branch=$(git branch --show-current 2>/dev/null)

    if [ -z "$branch" ]; then
        GIT_PROMPT=""
        return
    fi

    status=$(git status --porcelain 2>/dev/null)
    ahead=$(git rev-list --count '@{upstream}..HEAD' 2>/dev/null)
    behind=$(git rev-list --count 'HEAD..@{upstream}' 2>/dev/null)

    GIT_PROMPT=" $branch"

    if [ -n "$status" ]; then
        GIT_PROMPT+=" ✗"
    fi

    if [ "$ahead" -gt 0 ] 2>/dev/null; then
        GIT_PROMPT+=" ↑$ahead"
    fi

    if [ "$behind" -gt 0 ] 2>/dev/null; then
        GIT_PROMPT+=" ↓$behind"
    fi
}

update_prompt() {
    git_prompt

    PS1="\[\e[1;32m\]╭─ \$(date +%H:%M) · \u \[\e[33m\]\w \[\e[31m\]$GIT_PROMPT
\[\e[1;32m\]╰─❯ \[\e[0m\]"
}

PROMPT_COMMAND=update_prompt