import subprocess

from device import get_touch_device


class Injector:

    def __init__(self, serial, event_device=None):

        self.serial = serial
        self.event_device = event_device or get_touch_device(serial)

        self.process = subprocess.Popen(
            [
                "adb",
                "-s",
                serial,
                "shell",
                "su"
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )

        self.buffer = []

    def add(self, event_type, event_code, event_value):

        if self.process.poll() is not None:
            raise RuntimeError(f"su sessie is gestopt voor {self.serial}")

        self.buffer.append(
            f"sendevent {self.event_device} {event_type} {event_code} {event_value}"
        )

    def flush(self):

        if not self.buffer:
            return

        try:
            self.process.stdin.write(
                "\n".join(self.buffer) + "\n"
            )

            self.process.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise RuntimeError(f"Kan events niet verzenden naar {self.serial}") from exc

        self.buffer.clear()

    def close(self):

        try:
            if self.process.stdin and self.process.poll() is None:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

        self.process.terminate()
