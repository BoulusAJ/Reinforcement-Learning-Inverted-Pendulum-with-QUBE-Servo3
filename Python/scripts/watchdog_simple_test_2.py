import time
import numpy as np
from quanser.hardware import HIL

card = HIL("qube_servo3_usb", "0")  # (use your actual board name/id)
try:
    # configure expiration (if supported)
    chans = np.array([0], dtype=np.uint32)
    volts = np.array([0.0], dtype=np.float64)
    try:
        card.watchdog_set_analog_expiration_state(chans, int(chans.size), volts)
        print("expiration state configured")
    except Exception as e:
        print("expiration state not supported:", e)

    timeout = 0.05
    card.watchdog_start(timeout)
    print("watchdog started, now sleeping...")

    # IMPORTANT: do not call any card.* functions during this sleep
    time.sleep(0.5)

    # first call after the long sleep:
    expired = card.watchdog_is_expired()
    print("expired after sleep:", expired)

    reloaded_ok = card.watchdog_reload()
    print("reload returned:", reloaded_ok, "(False would mean it expired before reload)")

finally:
    try: card.watchdog_stop()
    except: pass
    card.close()
