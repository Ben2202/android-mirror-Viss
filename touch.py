import subprocess

_processes = {}


def listen_touch(master_serial):
    """
    Generator die touch-events van het master toestel teruggeeft.
    """

    print(f"\nLuisteren naar touch-events van {master_serial}...\n")

    process = subprocess.Popen(
        [
            "adb",
            "-s",
            master_serial,
            "shell",
            "getevent",
            "-lt"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    _processes[master_serial] = process

    try:
        if process.stdout is None:
            return

        for line in process.stdout:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) < 4:
                continue

            event = {
                "type": parts[-3],
                "code": parts[-2],
                "value": parts[-1]
            }

            if event["code"] not in (
                "ABS_MT_POSITION_X",
                "ABS_MT_POSITION_Y",
                "ABS_MT_TRACKING_ID",
                "ABS_MT_PRESSURE",
                "ABS_MT_TOUCH_MAJOR",
                "ABS_MT_TOUCH_MINOR",
                "ABS_MT_ORIENTATION",
                "ABS_MT_SLOT",
                "BTN_TOUCH",
                "SYN_REPORT"
            ):
                continue

            yield event

    finally:
        _processes.pop(master_serial, None)

        if process.poll() is None:
            try:
                process.kill()
            except OSError:
                pass


def stop_listening(master_serial=None):
    serials = [master_serial] if master_serial else list(_processes)

    for serial in serials:
        process = _processes.get(serial)
        if process is None or process.poll() is not None:
            continue

        try:
            process.terminate()
        except OSError:
            pass
