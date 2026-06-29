import subprocess

def detect_devices():
    devices = []

    result = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.strip().split("\n")[1:]

    for line in lines:
        if "\tdevice" in line:
            serial = line.split("\t")[0]

            model = subprocess.run(
                ["adb", "-s", serial, "shell", "getprop", "ro.product.model"],
                capture_output=True,
                text=True
            ).stdout.strip()

            devices.append({
                "model": model,
                "serial": serial
            })

    return devices