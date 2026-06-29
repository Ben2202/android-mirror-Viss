import subprocess


class Injector:

    def __init__(self, serial, event_device="/dev/input/event4"):

        self.serial = serial
        self.event_device = event_device

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

        self.buffer.append(
            f"sendevent {self.event_device} {event_type} {event_code} {event_value}"
        )


    def flush(self):

        if not self.buffer:
            return

        self.process.stdin.write(
            "\n".join(self.buffer) + "\n"
        )

        self.process.stdin.flush()

        self.buffer.clear()


    def close(self):

        try:

            self.process.stdin.write("exit\n")

            self.process.stdin.flush()

        except:

            pass

        self.process.terminate()