# Python/scripts/test_qube3_pal_200hz.py
import time
from rl_qube.interface.qube3_pal_interface import Qube3PALInterface

Ts = 0.005  # 200 Hz

io = Qube3PALInterface(
    frequency=200,
    motor_voltage_limit=2.0,     # conservative
    drop_old_samples=True,
)

io.open()

print("Running 200 Hz PAL loop (motor disabled)…")

try:
    next_t = time.perf_counter()

    for k in range(800):  # 4 seconds
        state = io.step(
            motor_voltage=0.0,
            motor_enable=False,          # keep safe for first test
            led_rgb=(False, True, False),   # green
        )

        if k % 20 == 0:
            print(
                f"k={k:03d} | "
                f"θ={state.theta:+.3f} rad | "
                f"φ={state.phi:+.3f} rad | "
                f"θ̇={state.theta_dot:+.2f} | "
                f"φ̇={state.phi_dot:+.2f} | "
                f"I={state.current:+.3f} A | "
                f"fault={state.fault} stall={state.stall_detect}/{state.stall_error}"
            )

        # keep the outer loop roughly aligned to 200 Hz
        next_t += Ts
        sleep = next_t - time.perf_counter()
        if sleep > 0:
            time.sleep(sleep)

finally:
    io.close()
    print("Stopped safely.")
