# watchdog_effect_test_qube3.py
import time
import numpy as np
from typing import Any, cast

from pal.products.qube import QubeServo3
from quanser.hardware.hil import HIL

from rl_qube.interface.qube3_pal_interface import to_float


def main():
    freq = 200
    timeout_s = 0.05
    v_cmd = 2.0

    q = QubeServo3(hardware=1, pendulum=1, frequency=freq, readMode=1)

    with q:
        card_any = getattr(q, "card", None)
        if card_any is None:
            raise RuntimeError("No HIL card available")
        card = cast(HIL, card_any)

        print("card:", type(card))
        print("read_task:", getattr(q, "_readTask", None))

        # Safe initial outputs
        q.write_voltage(0.0)
        q.write_led(np.array([0.0, 0.0, 0.0], dtype=np.float64))

        # Stop + clear watchdog (clean baseline)
        try:
            card.watchdog_stop()
        except Exception:
            pass

        try:
            card.watchdog_clear()
        except Exception:
            pass

        # Configure expiration state to 0V
        chans_raw = getattr(q, "WRITE_ANALOG_CHANNELS", None)
        print("WRITE_ANALOG_CHANNELS raw:", chans_raw)

        if chans_raw is not None:
            chans = np.asarray(chans_raw, dtype=np.uint32).reshape(-1)
            if chans.size > 0:
                volts = np.zeros(chans.size, dtype=np.float64)
                card.watchdog_set_analog_expiration_state(
                    chans, int(chans.size), volts
                )
                print("Configured analog expiration state to 0V on chans", chans.tolist())

        # === PRE-WATCHDOG STATE ===
        q.write_voltage(v_cmd)
        time.sleep(2)
        q.read_outputs()

        pos0 = to_float(getattr(q, "motorPosition", 0.0))
        speed0 = to_float(getattr(q, "motorSpeed", 0.0))
        current0 = to_float(getattr(q, "motorCurrent", 0.0))

        print(f"pre-watchdog: V={v_cmd:+.2f} | pos={pos0:+.3f} "
              f"speed={speed0:+.3f} | current={current0:+.3f} A")

        # === START WATCHDOG ===
        card.watchdog_start(float(timeout_s))
        print("watchdog_start done, timeout_s =", timeout_s)

        # Kick once
        r = card.watchdog_reload()
        e = card.watchdog_is_expired()
        print("kick once: reload returned", r, "expired?", e)

        # === LET IT EXPIRE ===
        print(f"sleeping {100*timeout_s:.3f}s without reload ...")
        time.sleep(100 * timeout_s)

        expired = card.watchdog_is_expired()
        reload_after = card.watchdog_reload()
        expired_after = card.watchdog_is_expired()

        print("after sleep:",
              "expired?", expired,
              "reload returned", reload_after,
              "expired after reload?", expired_after)

        # === TRY WRITING AFTER EXPIRY ===
        q.write_voltage(v_cmd)
        time.sleep(10)
        q.read_outputs()

        pos1 = to_float(getattr(q, "motorPosition", 0.0))
        speed1 = to_float(getattr(q, "motorSpeed", 0.0))
        current1 = to_float(getattr(q, "motorCurrent", 0.0))

        print(f"post-expiry write attempt: V={v_cmd:+.2f} | "
              f"pos={pos1:+.3f} (Δ={pos1-pos0:+.3f}) "
              f"speed={speed1:+.3f} | current={current1:+.3f} A")

        # === CLEAR WATCHDOG ===
        card.watchdog_clear()
        print("watchdog_clear called")

        # Try writing again
        q.write_voltage(v_cmd)
        time.sleep(0.1)
        q.read_outputs()

        pos2 = to_float(getattr(q, "motorPosition", 0.0))
        speed2 = to_float(getattr(q, "motorSpeed", 0.0))
        current2 = to_float(getattr(q, "motorCurrent", 0.0))

        print(f"after clear: V={v_cmd:+.2f} | "
              f"pos={pos2:+.3f} (Δ={pos2-pos1:+.3f}) "
              f"speed={speed2:+.3f} | current={current2:+.3f} A")

        # Stop watchdog cleanly
        card.watchdog_stop()
        print("watchdog_stop called")

        # Always leave safe
        q.write_voltage(0.0)
        q.write_led(np.array([1.0, 0.0, 0.0], dtype=np.float64))


if __name__ == "__main__":
    main()
