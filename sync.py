import threading

from touch import listen_touch, stop_listening
from parser import parse_event
from inject import close_all_injectors, send_event

running = False


def start_sync(master, followers):
    global running

    if running:
        return False

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

    return True


def stop_sync():
    global running

    was_running = running
    running = False
    stop_listening()
    close_all_injectors()
    print("SYNC GESTOPT")
    return was_running


def sync_loop(master, followers):
    global running

    try:
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
    finally:
        running = False
        close_all_injectors()
