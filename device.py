import subprocess
import re

_cache = {}


def get_touch_device(serial):
    """
    Zoek automatisch het juiste /dev/input/eventX
    waarop het touchscreen zit.
    """

    if serial in _cache:
        return _cache[serial]

    output = subprocess.check_output(
        [
            "adb",
            "-s",
            serial,
            "shell",
            "getevent",
            "-lp"
        ],
        text=True
    )

    current_device = None

    for line in output.splitlines():

        line = line.strip()

        m = re.match(r"add device \d+: (/dev/input/event\d+)", line)
        if m:
            current_device = m.group(1)
            continue

        if (
            "ABS_MT_POSITION_X" in line
            or "BTN_TOUCH" in line
        ):
            _cache[serial] = current_device
            print(f"{serial}: touch device = {current_device}")
            return current_device

    raise RuntimeError(f"Geen touchscreen gevonden voor {serial}")