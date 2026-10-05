# ============================================================
# SPINNER SHELL - EXPERIMENTAL
# ============================================================

# Cargar nuestra configuración habitual
source ~/.bashrc

# Evitar que el runner vuelva a ser interceptado
if [ "${SPINNER_SHELL_CHILD:-0}" != "1" ]; then

    spinner_debug() {
        local cmd="$BASH_COMMAND"
        local first_word
        local command_type

        # Ignorar comandos internos del prompt
        case "$cmd" in
            update_prompt|git_prompt|spinner_debug|source\ *|PROMPT_COMMAND*)
                return 0
                ;;
        esac

        # Primer elemento del comando
        first_word="${cmd%%[[:space:]]*}"

        # Qué es ese comando para Bash
        command_type=$(type -t -- "$first_word" 2>/dev/null)

        case "$command_type" in
            file|function|alias)
                ;;
            *)
                return 0
                ;;
        esac

        # Ejecutar mediante nuestro runner
        SPINNER_SHELL_CHILD=1 \
            python ~/.bash/command_runner.py "$cmd"

        # Evitar que Bash ejecute otra vez el comando original
        return 1
    }

    trap spinner_debug DEBUG
fi