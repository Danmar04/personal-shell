import os
import sys
import time


FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def format_elapsed(seconds):
    seconds = int(seconds)

    minutes, seconds = divmod(seconds, 60)

    if minutes > 0:
        return f"{minutes} min {seconds} s"

    return f"{seconds} s"


def main():
    if len(sys.argv) != 2:
        return

    state_file = sys.argv[1]

    # Esperar brevemente a que Bash escriba el fichero
    for _ in range(50):
        if os.path.exists(state_file):
            break

        time.sleep(0.01)

    if not os.path.exists(state_file):
        return

    try:
        with open(state_file, "r", encoding="utf-8") as file:
            command = file.readline().strip()
    except OSError:
        return

    start_time = time.monotonic()
    frame = 0

    try:
        while os.path.exists(state_file):
            elapsed = format_elapsed(time.monotonic() - start_time)

            text = (
                f"\r\033[2K"
                f"{FRAMES[frame]}  {command} · {elapsed}"
            )

            sys.stdout.write(text)
            sys.stdout.flush()

            frame = (frame + 1) % len(FRAMES)

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        # Limpiar la línea del spinner
        sys.stdout.write("\r\033[2K")
        sys.stdout.flush()


if __name__ == "__main__":
    main()