import threading

from touch import listen_touch
from parser import parse_event
from inject import send_event

running = False


def start_sync(master, followers):
    global running

    if running:
        return

    running = True

    print("=" * 50)
    print("SYNC GESTART")
    print("MASTER    :", master)
    print("FOLLOWERS :", followers)
    print("=" * 50)

    threading.Thread(
        target=sync_loop,
        args=(master, followers),
        daemon=True,
    ).start()


def stop_sync():
    global running
    running = False
    print("SYNC GESTOPT")


def sync_loop(master, followers):
    global running

    for event in listen_touch(master):

        if not running:
            break

        parsed = parse_event(event)

        if parsed is None:
            continue

        event_type, event_code, event_value = parsed

        for follower in followers:
            send_event(
                follower,
                event_type,
                event_code,
                event_value,
            )