import time
from rl_qube.interface.qube3_pal_interface import Qube3PALInterface

Ts = 0.005
V = 1.0          # still safe, but overcomes friction better than 0.3V
seg = 0.4        # seconds

io = Qube3PALInterface(frequency=200, motor_voltage_limit=2.0, drop_old_samples=True)
io.open()

print("Sign test (counts-based): +V, 0, -V, 0")
print(f"V={V}V seg={seg}s Ts={Ts}s")

def segment(v_cmd: float, duration_s: float, led):
    n = max(1, int(round(duration_s / Ts)))

    s = io.step(motor_voltage=v_cmd, motor_enable=True, led_rgb=led)
    c0 = s.motor_counts
    cps_sum = s.motor_cps

    for _ in range(1, n):
        s = io.step(motor_voltage=v_cmd, motor_enable=True, led_rgb=led)
        cps_sum += s.motor_cps
        time.sleep(Ts)

    c1 = s.motor_counts
    avg_cps = cps_sum / n
    return int(c0), int(c1), float(avg_cps), float(s.current)


try:
    for k in range(3):
        print(f"\nTrial {k+1}/3")

        c0, c1, avg_cps, I = segment(+V, seg, (False, True, False))
        print(f"  +V: c0={c0:7d} c1={c1:7d} Δ={c1-c0:+6d} avgCPS={avg_cps:+8.1f} I~{I:+.3f}A")

        segment(0.0, seg, (True, True, False))

        c0, c1, avg_cps, I = segment(-V, seg, (False, False, True))
        print(f"  +V: c0={c0:7d} c1={c1:7d} Δ={c1-c0:+6d} avgCPS={avg_cps:+8.1f} I~{I:+.3f}A")

        segment(0.0, seg, (True, True, False))

finally:
    io.close()
    print("Stopped safely.")
