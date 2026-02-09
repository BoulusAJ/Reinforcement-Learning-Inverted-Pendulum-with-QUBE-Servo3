# Python/scripts/test_qube3_pal_enable_zero.py

import time
from rl_qube.interface.qube3_pal_interface import Qube3PALInterface

Ts = 0.005

io = Qube3PALInterface(frequency=200, motor_voltage_limit=2.0, drop_old_samples=True)
io.open()

print("Enabling motor (0V command). Touch nothing; listen for noise/jitter.")
print("Press Ctrl+C to stop.")

try:
    next_t = time.perf_counter()
    for k in range(400):  # 2 seconds
        s = io.step(
            motor_voltage=0.0,
            motor_enable=True,          # ENABLED
            led_rgb=(True, True, False) # yellow = enabled
        )

        if k % 20 == 0:
            print(
                f"k={k:03d} | θ={s.theta:+.3f} φ={s.phi:+.3f} | "
                f"θ̇={s.theta_dot:+.2f} φ̇={s.phi_dot:+.2f} | I={s.current:+.3f}A | "
                f"fault={s.fault}"
            )

        next_t += Ts
        dt = next_t - time.perf_counter()
        if dt > 0:
            time.sleep(dt)

finally:
    io.close()
    print("Stopped safely.")
