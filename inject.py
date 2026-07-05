from device import get_touch_device
from injector import Injector

_injectors = {}


def send_event(serial, event_type, event_code, event_value):
    """
    Stuur één Linux input-event naar een Android toestel.
    """

    try:
        injector = _injectors.get(serial)
        if injector is None:
            injector = Injector(serial, get_touch_device(serial))
            _injectors[serial] = injector

        injector.add(event_type, event_code, event_value)
        injector.flush()
    except Exception as e:
        print(f"[{serial}] Fout bij verzenden event: {e}")
        close_injector(serial)


def close_injector(serial):
    injector = _injectors.pop(serial, None)
    if injector is None:
        return

    injector.close()


def close_all_injectors():
    for serial in list(_injectors):
        close_injector(serial)
