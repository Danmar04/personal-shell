import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


MAVEN_HOME = Path(
    r"C:\Desarrollo\software\Maven\apache-maven-3.9.16-bin\apache-maven-3.9.16"
)

MAVEN_CMD = MAVEN_HOME / "bin" / "mvn.cmd"

LOG_DIR = Path(r"C:\Desarrollo\logs")


GREEN = "\033[0;32m"
RED = "\033[0;31m"
CYAN = "\033[0;36m"
RESET = "\033[0m"


SPINNER = [
    "⠋",
    "⠙",
    "⠹",
    "⠸",
    "⠼",
    "⠴",
    "⠦",
    "⠧",
    "⠇",
    "⠏",
]


def command_display(args):
    command = "mvn"

    for arg in args:
        if " " in arg:
            command += f' "{arg}"'
        else:
            command += f" {arg}"

    return command


def format_elapsed(seconds):
    seconds = int(seconds)

    minutes, seconds = divmod(seconds, 60)

    if minutes > 0:
        return f"{minutes} min {seconds} s"

    return f"{seconds} s"


def print_spinner(command, index, elapsed):
    frame = SPINNER[index % len(SPINNER)]
    elapsed_text = format_elapsed(elapsed)

    sys.stdout.write(
        f"\r\033[2K"
        f"{frame}  {command} · {elapsed_text}"
    )

    sys.stdout.flush()


def print_final_line(symbol, command, elapsed):
    elapsed_text = format_elapsed(elapsed)

    sys.stdout.write(
        f"\r\033[2K"
        f"{symbol}  {command} · {elapsed_text}\n"
    )

    sys.stdout.flush()


def clear_spinner():
    sys.stdout.write("\r\033[2K")
    sys.stdout.flush()


def show_success(log_file, elapsed):
    print(f"{GREEN}✓ Maven terminado correctamente{RESET}")
    print()
    print(f"Tiempo: {format_elapsed(elapsed)}")
    print()

    print("Resumen:")
    print("----------------------------------------")

    lines = log_file.read_text(
        encoding="utf-8",
        errors="replace"
    ).splitlines()

    show = False

    for line in lines:
        if "[INFO] BUILD SUCCESS" in line:
            show = True

        if show:
            print(line)

        if show and "[INFO] Finished at:" in line:
            break

    print("----------------------------------------")
    print()

    windows_log_path = str(log_file).replace("\\", "/")

    print("Log completo:")
    print(f"  {windows_log_path}")


def show_failure(log_file, elapsed):
    print(f"{RED}✗ Maven ha fallado{RESET}")
    print()
    print(f"Tiempo: {format_elapsed(elapsed)}")
    print()

    lines = log_file.read_text(
        encoding="utf-8",
        errors="replace"
    ).splitlines()

    # ========================================================
    # RESUMEN DE MAVEN
    # ========================================================

    reactor_start = None

    for i, line in enumerate(lines):
        if "[INFO] Reactor Summary" in line:
            reactor_start = i
            break

    if reactor_start is not None:
        # Mostrar las 30 líneas anteriores al Reactor Summary
        context_start = max(0, reactor_start - 30)

        print("Detalle del error:")
        print("----------------------------------------")

        for line in lines[context_start:reactor_start]:
            print(line)

        print("----------------------------------------")
        print()

        print("Resumen de Maven:")
        print("----------------------------------------")

        for line in lines[reactor_start:]:
            print(line)

            if "[INFO] Finished at:" in line:
                break

        print("----------------------------------------")
        print()

    # ========================================================
    # LOG COMPLETO
    # ========================================================

    windows_log_path = str(log_file).replace("\\", "/")

    print(f"{RED}Log completo disponible en:{RESET}")
    print(f"  {windows_log_path}")


def main():
    args = sys.argv[1:]
    command = command_display(args)

    # Maven version: ejecutar directamente sin spinner ni log
    if args and args[0] in ("-version", "--version"):
        result = subprocess.run(
            [str(MAVEN_CMD)] + args
        )

        return result.returncode

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = LOG_DIR / f"maven-{timestamp}.log"

    print()

    process = None
    start_time = time.monotonic()
    result = 1

    try:
        with open(
            log_file,
            "w",
            encoding="utf-8",
            errors="replace"
        ) as log:

            process = subprocess.Popen(
                [str(MAVEN_CMD)] + args,
                stdout=log,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )

            index = 0

            while process.poll() is None:
                elapsed = time.monotonic() - start_time

                print_spinner(
                    command,
                    index,
                    elapsed
                )

                index += 1

                # Actualizar el spinner una vez por segundo
                time.sleep(0.2)

            result = process.returncode

    except KeyboardInterrupt:
        clear_spinner()

        elapsed = time.monotonic() - start_time

        print_final_line(
            "✗",
            f"{command} — cancelado",
            elapsed
        )

        if process is not None and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=3)

            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

        print()
        print(f"{RED}✗ Maven cancelado por el usuario{RESET}")
        print()
        print(f"Tiempo: {format_elapsed(elapsed)}")
        print()
        print("Log parcial:")

        windows_log_path = str(log_file).replace("\\", "/")

        print(f"  {windows_log_path}")

        return 130

    finally:
        clear_spinner()

    elapsed = time.monotonic() - start_time

    if result == 0:
        print_final_line(
            "✓",
            command,
            elapsed
        )
    else:
        print_final_line(
            "✗",
            command,
            elapsed
        )

    print()

    if result == 0:
        show_success(
            log_file,
            elapsed
        )

        try:
            import winsound

            winsound.Beep(
                1000,
                300
            )

        except Exception:
            pass

        return 0

    show_failure(
        log_file,
        elapsed
    )

    try:
        import winsound

        winsound.Beep(
            300,
            700
        )

    except Exception:
        pass

    return result


if __name__ == "__main__":
    sys.exit(main())