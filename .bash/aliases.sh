# ============================================================
# ALIASES BÁSICOS
# ============================================================

alias ll='ls -lah'
alias reload_bashrc='source ~/.bashrc'
alias edit_bashrc='code ~/.bashrc'
alias ..='cd ..'


# ============================================================
# NAVEGACIÓN
# ============================================================

cd() {
    builtin cd "$@" && ll
}

home() {
    cd C:/Desarrollo
}


# ============================================================
# SCRIPTS / HERRAMIENTAS
# ============================================================

alias compilarLibsCore='python "C:/Desarrollo/proyectos/CORE/repositories/commons-libs/compilarLibs.py"'

alias crear-mr='python "C:/Desarrollo/herramientas/creacion-mrs/creacion-mr.py"'

alias fichar='python "C:/Desarrollo/herramientas/fichaje/fichar.py"'

alias desfichar='python "C:/Desarrollo/herramientas/fichaje/desfichar.py"'

alias get-versions='python "C:/Desarrollo/herramientas/get-versions/get-versions.py"'