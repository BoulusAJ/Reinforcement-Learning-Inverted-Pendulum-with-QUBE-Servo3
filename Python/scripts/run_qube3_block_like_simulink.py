# run_qube3_block_like_simulink.py
"""
Run the same logic as the Simulink Python Code block, but outside Simulink.

Lifecycle mapping:
  - Initialize tab   -> start()
  - Output tab       -> step(u, enable) each Ts
  - Terminate tab    -> stop()

This is best-effort timing on Windows (not hard real-time).
The QUBE task-based IO still samples at the requested frequency in the background.
"""

from __future__ import annotations

import math
import time
from typing import Callable

import numpy as np
from rl_qube.simulink.qube3_block import step_1, start
from rl_qube.simulink.qube3_block import start, step, stop, step_1


def make_command_profile(mode: str, Ts: float) -> Callable[[float], float]:
    """
    Returns a function u(t)->command in [-1,1] (or in volts depending on your step()).
    Adjust as needed.
    """
    mode = mode.lower()

    if mode == "zero":
        return lambda t: 0.0

    if mode == "sine":
        # small sine command
        amp = 0.5
        freq_hz = 0.5
        return lambda t: amp * math.sin(2.0 * math.pi * freq_hz * t)

    if mode == "random":
        # small Gaussian noise, held each step
        scale = 0.15
        rng = np.random.default_rng(0)

        def u_of_t(_t: float) -> float:
            return float(scale * rng.standard_normal())

        return u_of_t

    raise ValueError(f"Unknown mode: {mode}")


def run(
    frequency: int = 200,
    vlimit: float = 1.0,
    seconds: float = 10.0,
    enable_after_s: float = 0.5,
    mode: str = "zero",
    print_every: int = 50,
) -> None:
    Ts = 1.0 / float(frequency)
    u_of_t = make_command_profile(mode, Ts)

    print("Starting (Simulink-block equivalent)...")
    print(f"  frequency = {frequency} Hz (Ts={Ts:.6f}s)")
    print(f"  vlimit    = {vlimit} V (enforced inside interface)")
    print(f"  duration  = {seconds} s")
    print(f"  mode      = {mode}")
    print("  Ctrl+C to stop.\n")

    start(frequency=frequency, vlimit=vlimit)

    t0 = time.perf_counter()
    t_next = t0
    k = 0

    try:
        while True:
            now = time.perf_counter()
            t = now - t0

            if t >= seconds:
                break

            enable = 1 if t >= enable_after_s else 0
            u = u_of_t(t) if enable else 0.0

            # This mirrors the Simulink Output tab call
            # Expected tuple:
            # (theta, phi, theta_dot, phi_dot, current, fault, backlog, rt_ok)
            out = step_1(u, enable)
            #out = step(u, enable)

            # Be tolerant to your current signature (6 outputs vs extended)
            theta = float(out[0])
            phi = float(out[1])
            theta_dot = float(out[2])
            phi_dot = float(out[3])
            current = float(out[4])
            fault = int(out[5])

            backlog = int(out[6]) if len(out) > 6 else -1
            rt_ok = bool(out[7]) if len(out) > 7 else True

            if (k % print_every) == 0:
                print(
                    f"t={t:7.3f}s "
                    f"en={enable} u={u:+.3f} | "
                    f"th={theta:+.3f} ph={phi:+.3f} | "
                    f"thd={theta_dot:+.3f} phd={phi_dot:+.3f} | "
                    f"I={current:+.3f}A fault={fault} "
                    f"backlog={backlog} rt_ok={rt_ok}"
                )

            # Optional: fail-safe stop if fault
            #if fault != 0 or (len(out) > 7 and not rt_ok):
            if fault != 0:
                print("fault: ", fault, " len(out): ", len(out))
                print("\nFault/rt violation detected -> stopping safely.")
                break

            # Best-effort pacing to Ts (similar to trying to run in real-time)
            t_next += Ts
            sleep_s = t_next - time.perf_counter()
            if sleep_s > 0:
                time.sleep(sleep_s)
            else:
                # We're late; do not sleep. (You can also record lateness here.)
                pass

            k += 1

    except KeyboardInterrupt:
        print("\nCtrl+C received -> stopping safely.")

    finally:
        stop()
        print("Stopped.")


if __name__ == "__main__":
    run(
        frequency=200,
        vlimit=1.0,      # start safe; increase later if needed
        seconds=10.0,
        enable_after_s=1.0,
        mode="sine",   # "zero" | "sine" | "random"
        print_every=50,
    )
