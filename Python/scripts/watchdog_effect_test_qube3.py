# watchdog_effect_test_qube3.py
import time
import numpy as np

from pal.products.qube import QubeServo3
from quanser.hardware import HIL

import numpy as np
from typing import Any

from rl_qube.interface.qube3_pal_interface import to_float

def to_float(x: Any) -> float:
    if isinstance(x, np.ndarray):
        if x.size == 0:
            return 0.0
        return float(x.reshape(-1)[0])
    return float(x)


def main():
    freq = 200
    timeout_s = 0.05
    v_cmd = 1.0

    q = QubeServo3(hardware=1, pendulum=1, frequency=freq, readMode=1)

    with q:
        card = getattr(q, "card", None)
        read_task = getattr(q, "_readTask", None)

        print("card:", type(card))
        print("read_task:", read_task)

        # Safe LED off, voltage 0
        q.write_voltage(0.0)
        q.write_led(np.array([0.0, 0.0, 0.0], dtype=np.float64))

        # Best-effort: stop/clear any previous watchdog state
        try:
            card.watchdog_stop()
        except Exception as e:
            print("watchdog_stop:", e)
        try:
            card.watchdog_clear()
        except Exception as e:
            print("watchdog_clear:", e)

        # Configure expiration state to 0V on analog out channel(s)
        chans_raw = getattr(q, "WRITE_ANALOG_CHANNELS", None)
        print("WRITE_ANALOG_CHANNELS raw:", chans_raw)

        if chans_raw is not None:
            chans = np.asarray(chans_raw, dtype=np.uint32).reshape(-1)
            if chans.size > 0:
                volts = np.zeros(chans.size, dtype=np.float64)
                try:
                    card.watchdog_set_analog_expiration_state(chans, int(chans.size), volts)
                    print("Configured analog expiration state to 0V on chans", chans.tolist())
                except Exception as e:
                    print("watchdog_set_analog_expiration_state failed:", e)

        # Write nonzero command BEFORE starting watchdog
        q.write_voltage(v_cmd)
        q.read_outputs()
        i0 = to_float(getattr(q, "motorCurrent", 0.0))
        print(f"pre-watchdog: wrote {v_cmd:+.2f} V, motorCurrent={i0:+.3f} A")

        # Start watchdog
        card.watchdog_start(float(timeout_s))
        print("watchdog_start done, timeout_s =", timeout_s)

        # Kick once
        r = card.watchdog_reload()
        e = bool(card.watchdog_is_expired())
        print("kick once: reload returned", r, "expired?", e)

        # Now: do NOT reload; sleep past timeout
        print(f"sleeping {10*timeout_s:.3f}s without reload ...")
        time.sleep(10 * timeout_s)

        # Observe flags
        e1 = bool(card.watchdog_is_expired())
        r1 = card.watchdog_reload()
        e2 = bool(card.watchdog_is_expired())
        print("after sleep: expired?", e1, "reload returned", r1, "expired after reload?", e2)

        # Try writing again (should be ignored if watchdog expired+locked outputs)
        try:
            q.write_voltage(v_cmd)
            print("post-sleep: write_voltage succeeded (call returned)")
        except Exception as e:
            print("post-sleep: write_voltage raised:", e)

        q.read_outputs()
        i1 = to_float(getattr(q, "motorCurrent", 0.0))
        print(f"post-sleep: motorCurrent={i1:+.3f} A")

        # Try clearing watchdog state (if it expired)
        try:
            card.watchdog_clear()
            print("watchdog_clear called")
        except Exception as e:
            print("watchdog_clear failed:", e)

        # Try writing again after clear
        q.write_voltage(v_cmd)
        q.read_outputs()
        i2 = to_float(getattr(q, "motorCurrent", 0.0))
        print(f"after clear: wrote {v_cmd:+.2f} V, motorCurrent={i2:+.3f} A")

        # Stop watchdog
        try:
            card.watchdog_stop()
            print("watchdog_stop called")
        except Exception as e:
            print("watchdog_stop failed:", e)

        # Always leave safe
        q.write_voltage(0.0)
        q.write_led(np.array([1.0, 0.0, 0.0], dtype=np.float64))

if __name__ == "__main__":
    main()
