# run_qube3_block_like_simulink.py
"""
Run the same logic as the Simulink Python Code block, but outside Simulink.

Lifecycle mapping:
  - Initialize tab   -> start()
  - Output tab       -> step(u, enable) each Ts
  - Terminate tab    -> stop()

This is best-effort timing on Windows (not hard real-time).
The QUBE task-based IO still samples at the requested frequency in the background.

Supports two call modes:
  - step():     8 outputs (legacy)
  - step_mon(): 12 outputs (adds dt_wall, miss_count, overflow_delta, faulted)
"""

from __future__ import annotations

import math
import time
from typing import Callable, Literal, Tuple

import numpy as np
from rl_qube.simulink.qube3_block import start, step, stop, step_mon


def make_command_profile(mode: str, Ts: float) -> Callable[[float], float]:
    """
    Returns a function u(t)->command in [-1,1] (or in volts depending on your step()).
    Adjust as needed.
    """
    mode = mode.lower()

    if mode == "zero":
        return lambda t: 0.0

    if mode == "sine":
        amp = 0.5
        freq_hz = 0.5
        return lambda t: amp * math.sin(2.0 * math.pi * freq_hz * t)

    if mode == "random":
        scale = 0.15
        rng = np.random.default_rng(0)

        def u_of_t(_t: float) -> float:
            return float(scale * rng.standard_normal())

        return u_of_t

    raise ValueError(f"Unknown mode: {mode}")


def _parse_outputs(out: Tuple[float, ...]) -> dict:
    """
    Parses either 8-output (step) or 12-output (step_mon) tuples.
    Returns a uniform dict with optional monitoring fields defaulted safely.
    """
    if len(out) < 6:
        raise RuntimeError(f"Unexpected output length {len(out)}: {out}")

    theta = float(out[0])
    phi = float(out[1])
    theta_dot = float(out[2])
    phi_dot = float(out[3])
    current = float(out[4])
    fault = int(out[5])

    backlog = int(out[6]) if len(out) > 6 else -1
    rt_ok = bool(int(out[7])) if len(out) > 7 else True

    # Monitoring extras (step_mon)
    dt_wall = float(out[8]) if len(out) > 8 else float("nan")
    miss_count = int(out[9]) if len(out) > 9 else 0
    overflow_delta = int(out[10]) if len(out) > 10 else 0
    faulted = bool(int(out[11])) if len(out) > 11 else False

    return dict(
        theta=theta,
        phi=phi,
        theta_dot=theta_dot,
        phi_dot=phi_dot,
        current=current,
        fault=fault,
        backlog=backlog,
        rt_ok=rt_ok,
        dt_wall=dt_wall,
        miss_count=miss_count,
        overflow_delta=overflow_delta,
        faulted=faulted,
    )


def run(
    frequency: int = 200,
    vlimit: float = 1.0,
    seconds: float = 10.0,
    enable_after_s: float = 0.5,
    mode: str = "zero",
    print_every: int = 50,
    *,
    call_mode: Literal["step", "step_mon"] = "step_mon",
    dt_hard_limit_mult: float = 10.0,
    overflow_hard_limit: int = 5,
    enable_watchdog: bool = True,
) -> None:
    Ts = 1.0 / float(frequency)
    u_of_t = make_command_profile(mode, Ts)

    print("Starting (Simulink-block equivalent)...")
    print(f"  frequency = {frequency} Hz (Ts={Ts:.6f}s)")
    print(f"  vlimit    = {vlimit} V (enforced inside interface)")
    print(f"  duration  = {seconds} s")
    print(f"  mode      = {mode}")
    print(f"  call_mode = {call_mode}")
    print(f"  dt_hard_limit_mult = {dt_hard_limit_mult} (=> {dt_hard_limit_mult*Ts:.6f}s)")
    print(f"  overflow_hard_limit = {overflow_hard_limit}")
    print(f"  watchdog  = {enable_watchdog}")
    print("  Ctrl+C to stop.\n")

    start(
        frequency=frequency,
        vlimit=vlimit,
        dt_hard_limit_mult=dt_hard_limit_mult,
        overflow_hard_limit=overflow_hard_limit,
        enable_watchdog=enable_watchdog,
    )

    # Use perf_counter for host pacing; monotonic and high-res
    t0 = time.perf_counter()
    t_next = t0

    # Host-side pacing stats (separate from device-side dt_wall)
    late_max = 0.0
    late_count = 0

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
            if call_mode == "step":
                out = step(u, enable)
            else:
                out = step_mon(u, enable)

            s = _parse_outputs(out)

            if (k % print_every) == 0:
                # Host lateness = how far past the scheduled tick we are
                late = max(0.0, time.perf_counter() - t_next)
                late_max = max(late_max, late)
                if late > 0.0:
                    late_count += 1

                # Show monitoring only if present
                if call_mode == "step_mon":
                    print(
                        f"t={t:7.3f}s "
                        f"en={enable} u={u:+.3f} | "
                        f"th={s['theta']:+.3f} ph={s['phi']:+.3f} | "
                        f"thd={s['theta_dot']:+.3f} phd={s['phi_dot']:+.3f} | "
                        f"I={s['current']:+.3f}A fault={s['fault']} "
                        f"backlog={s['backlog']} rt_ok={s['rt_ok']} | "
                        f"dt_wall={s['dt_wall']*1000.0:7.3f}ms "
                        f"miss={s['miss_count']:d} ovf_d={s['overflow_delta']:d} "
                        f"faulted={int(s['faulted'])} | "
                        f"host_late={late*1000.0:6.2f}ms"
                    )
                else:
                    print(
                        f"t={t:7.3f}s "
                        f"en={enable} u={u:+.3f} | "
                        f"th={s['theta']:+.3f} ph={s['phi']:+.3f} | "
                        f"thd={s['theta_dot']:+.3f} phd={s['phi_dot']:+.3f} | "
                        f"I={s['current']:+.3f}A fault={s['fault']} "
                        f"backlog={s['backlog']} rt_ok={s['rt_ok']}"
                    )

            # Stop conditions:
            # - interface fault latch (faulted) indicates it is already returning zeros
            # - hardware fault flag (fault != 0)
            # - rt_ok false indicates backlog policy triggered (legacy)
            if s["faulted"]:
                print("\nFAULT LATCH active (faulted=1) -> stopping safely.")
                break
            if s["fault"] != 0:
                print("\nHardware fault flag (fault!=0) -> stopping safely.")
                break
            if not s["rt_ok"]:
                print("\nrt_ok=0 -> stopping safely.")
                break

            # Best-effort pacing to Ts
            t_next += Ts
            sleep_s = t_next - time.perf_counter()
            if sleep_s > 0:
                time.sleep(sleep_s)
            else:
                # we're late: track it, do not sleep
                late = -sleep_s
                late_max = max(late_max, late)
                late_count += 1

            k += 1

    except KeyboardInterrupt:
        print("\nCtrl+C received -> stopping safely.")

    finally:
        stop()
        print("Stopped.")
        if k > 0:
            print(
                f"Host pacing stats: late_count={late_count}/{k} "
                f"late_max={late_max*1000.0:.2f}ms"
            )


if __name__ == "__main__":
    run(
        frequency=200,
        vlimit=1.0,          # start safe; increase later if needed
        seconds=2,
        enable_after_s=1.0,
        mode="sine",         # "zero" | "sine" | "random"
        print_every=50,
        call_mode="step_mon", # "step" | "step_mon"
        dt_hard_limit_mult=10.0
    )
