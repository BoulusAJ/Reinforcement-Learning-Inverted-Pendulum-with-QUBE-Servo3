import time
from rl_qube.interface.qube3_pal_interface import Qube3PALInterface

Ts = 0.005
V = 0.3          # small and safe
pulse_len = 0.25 # seconds
hold_len = 0.25  # seconds

io = Qube3PALInterface(frequency=200, motor_voltage_limit=2.0, drop_old_samples=True)
io.open()

print("Pulse test: +V, 0, -V, 0 (repeat). Keep hand near E-stop / be ready to Ctrl+C.")
print(f"V={V}V, pulse={pulse_len}s, hold={hold_len}s")

def run_segment(duration_s: float, v_cmd: float, led):
    # Ensure at least 1 tick
    n = max(1, int(round(duration_s / Ts)))

    # Take first sample
    s = io.step(motor_voltage=v_cmd, motor_enable=True, led_rgb=led)
    theta0 = s.theta

    # Run remaining ticks
    for k in range(1, n):
        s = io.step(motor_voltage=v_cmd, motor_enable=True, led_rgb=led)
        if k % 20 == 0:
            print(f"  v={v_cmd:+.2f} | θ={s.theta:+.3f} φ={s.phi:+.3f} | I={s.current:+.3f}A")
        time.sleep(Ts)

    return float(theta0), float(s.theta)

try:
    for cycle in range(3):
        print(f"\nCycle {cycle+1}/3")

        t0, t1 = run_segment(pulse_len, +V, (False, True, False))  # green
        print(f"  Δθ ( +V ) = {t1 - t0:+.3f} rad")

        run_segment(hold_len, 0.0, (True, True, False))            # yellow

        t0, t1 = run_segment(pulse_len, -V, (False, False, True))  # blue
        print(f"  Δθ ( -V ) = {t1 - t0:+.3f} rad")

        run_segment(hold_len, 0.0, (True, True, False))            # yellow

finally:
    io.close()
    print("Stopped safely.")
