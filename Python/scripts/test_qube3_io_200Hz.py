# Python/scripts/test_qube3_io_200hz.py
import time
from rl_qube.interface import Qube3IO

io = Qube3IO(dt=0.005)
io.open()

try:
    for k in range(20000):  # 1 second at 200 Hz
        r = io.step(motor_voltage=0.0, motor_enable=True)
        if k % 20 == 0:
            print(
                f"theta={r.theta:+.3f} rad, phi={r.phi:+.3f} rad, "
                f"theta_dot={r.theta_dot:+.2f} rad/s, phi_dot={r.phi_dot:+.2f} rad/s"
            )
        time.sleep(0.005)
finally:
    io.close()
