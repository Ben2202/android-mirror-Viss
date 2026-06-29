import subprocess

from device import get_touch_device


def send_event(serial, event_type, event_code, event_value):
    """
    Stuur één Linux input-event naar een Android toestel.
    """

    device = get_touch_device(serial)

    subprocess.run(
        [
            "adb",
            "-s",
            serial,
            "shell",
            "su",
            "-c",
            f"sendevent {device} {event_type} {event_code} {event_value}",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )