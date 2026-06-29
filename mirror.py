import subprocess


def start_mirror(serial):
    """
    Start één scrcpy-venster.
    """
    subprocess.Popen([
        "scrcpy",
        "-s",
        serial
    ])


def start_multiple(serials):
    """
    Start meerdere scrcpy-vensters.
    """
    for serial in serials:
        start_mirror(serial)