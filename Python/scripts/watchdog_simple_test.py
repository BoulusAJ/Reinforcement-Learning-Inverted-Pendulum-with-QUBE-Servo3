import time
from quanser.hardware import HIL, HILError
card = HIL("qube_servo3_usb", "0")
try:
    timeout = 0.1
    card.watchdog_start(timeout)
    time.sleep(0.01)
    for i in range(50):
        is_watchdog_expired = card.watchdog_is_expired()
        time.sleep(0.1)
        print(is_watchdog_expired)
        if is_watchdog_expired:
            break
    # ...

except HILError as h:
    print(h.get_error_message())
finally:
    card.close()