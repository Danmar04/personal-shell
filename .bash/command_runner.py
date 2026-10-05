import signal
import subprocess
import sys
import threading
import time


FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

running = True
process = None
command = ""
start_time = 0


def format_elapsed(seconds):
    seconds = int(seconds)

    minutes, seconds = divmod(seconds, 60)

    if minutes > 0:
        return f"{minutes} min {seconds} s"

    return f"{seconds} s"


def draw_spinner(frame):
    elapsed = format_elapsed(time.monotonic() - start_time)

    sys.stdout.write(
        f"\r\033[2K"
        f"{FRAMES[frame]}  {command} · {elapsed}"
    )

    sys.stdout.flush()


def spinner():
    frame = 0

    while running:
        draw_spinner(frame)

        frame = (frame + 1) % len(FRAMES)

        time.sleep(0.1)


def handle_ctrl_c(signum, frame):
    global running

    running = False

    if process is not None:
        try:
            process.send_signal(signal.SIGINT)
        except Exception:
            pass


def main():
    global process
    global running
    global command
    global start_time

    if len(sys.argv) < 2:
        print('Uso: command_runner.py "comando"')
        sys.exit(1)

    command = sys.argv[1]
    start_time = time.monotonic()

    signal.signal(signal.SIGINT, handle_ctrl_c)

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        spinner_thread = threading.Thread(
            target=spinner,
            daemon=True,
        )

        spinner_thread.start()

        output, _ = process.communicate()

        return_code = process.returncode

    except KeyboardInterrupt:
        handle_ctrl_c(None, None)

        if process is not None:
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()

        return_code = 130
        output = ""

    finally:
        running = False

        if 'spinner_thread' in locals():
            spinner_thread.join(timeout=1)

        # Tiempo final
        elapsed = format_elapsed(time.monotonic() - start_time)

        # Dejar fija la línea final del spinner
        sys.stdout.write(
            f"\r\033[2K"
            f"✓  {command} · {elapsed}\n"
        )

        # Mostrar la salida del comando debajo
        if output:
            sys.stdout.write(output)

            if not output.endswith("\n"):
                sys.stdout.write("\n")

        sys.stdout.flush()

    sys.exit(return_code)


if __name__ == "__main__":
    main()