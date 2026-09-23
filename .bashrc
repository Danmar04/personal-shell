# =========================
# Aliases
# =========================

alias ll='ls -lah'
alias reload_bashrc='source ~/.bashrc'
alias edit_bashrc='code ~/.bashrc'
alias ..='cd ..'


# =========================
# Aliases - scripts python
# =========================
alias compilarLibsCore='python "C:/Desarrollo/proyectos/CORE/commons-libs/compilarLibs.py"'
alias crear-mr='python "C:/Desarrollo/herramientas/creacion-mrs/creacion-mr.py"'
alias fichar='python "C:/Desarrollo/herramientas/fichaje/fichar.py"'
alias desfichar='python "C:/Desarrollo/herramientas/fichaje/desfichar.py"'
alias get-versions='python "C:/Desarrollo/herramientas/get-versions/get-versions.py"'



# =========================
# CD personalizado
# =========================

cd() {
    builtin cd "$@" && ll
}


# =========================
# Directorio HOME de trabajo
# =========================

home() {
    cd C:/Desarrollo
}

# =========================
# Git prompt
# =========================

git_prompt() {
    local branch status ahead behind

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


mvn() {
    command mvn "$@"
    local result=$?

    if [ $result -eq 0 ]; then
        powershell.exe -NoProfile -Command "[console]::beep(1000,300)"
    else
        powershell.exe -NoProfile -Command "[console]::beep(300,700)"
    fi

    return $result
}

PROMPT_COMMAND=update_prompt


## PATH

export MAVEN_HOME="/c/Desarrollo/software/Maven/apache-maven-3.9.16-bin/apache-maven-3.9.16"
export PATH="$MAVEN_HOME/bin:$PATH"
