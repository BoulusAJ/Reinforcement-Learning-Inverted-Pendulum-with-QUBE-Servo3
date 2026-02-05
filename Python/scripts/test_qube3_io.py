# from Interface.qube3_io import Qube3IO
from rl_qube.interface import Qube3IO
import time

io = Qube3IO()
io.open()

try:
    for _ in range(5):
        r = io.step(motor_voltage=0.0, motor_enable=True)
        print(r)
        time.sleep(0.1)
finally:
    io.close()
