EVENT_TYPES = {
    "EV_SYN": 0,
    "EV_KEY": 1,
    "EV_ABS": 3,
}

# Alleen de events die echt nodig zijn
EVENT_CODES = {
    "SYN_REPORT": 0,

    "BTN_TOUCH": 330,

    "ABS_MT_SLOT": 47,
    "ABS_MT_TOUCH_MAJOR": 48,
    "ABS_MT_TOUCH_MINOR": 49,
    "ABS_MT_ORIENTATION": 52,
    "ABS_MT_POSITION_X": 53,
    "ABS_MT_POSITION_Y": 54,
    "ABS_MT_PRESSURE": 58,
    "ABS_MT_TRACKING_ID": 57,
}


def parse_event(event):
    """
    Zet een getevent om naar een sendevent.
    Retourneert:
        (event_type, event_code, event_value)
    """

    event_type_name = event.get("type")
    event_code_name = event.get("code")
    value = event.get("value")

    if event_type_name not in EVENT_TYPES:
        return None

    if event_code_name not in EVENT_CODES:
        return None

    event_type = EVENT_TYPES[event_type_name]
    event_code = EVENT_CODES[event_code_name]

    if value == "DOWN":
        value = 1
    elif value == "UP":
        value = 0
    else:
        try:
            value = int(value, 16)
        except ValueError:
            return None

    return (
        event_type,
        event_code,
        value
    )
