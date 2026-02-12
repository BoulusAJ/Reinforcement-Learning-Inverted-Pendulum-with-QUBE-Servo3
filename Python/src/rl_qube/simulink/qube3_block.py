from __future__ import annotations

from typing import Optional
from rl_qube.interface.qube3_pal_interface import Qube3PALInterface

_IO: Optional[Qube3PALInterface] = None


def start(
    frequency: int = 200,
    vlimit: float = 2.0,
    *,
    dt_hard_limit_mult: float = 10.0,
    overflow_hard_limit: int = 5,
    enable_watchdog: bool = True,
) -> None:
    """
    Initialize and open the Qube3 interface (singleton).

    Extra safety/monitoring params are keyword-only so existing calls don't break.
    """
    global _IO
    if _IO is None:
        _IO = Qube3PALInterface(
            frequency=frequency,
            motor_voltage_limit=vlimit,
            drop_old_samples=True,  # kept for compat; determinism now uses overflow counter + dt_wall
            dt_hard_limit_mult=dt_hard_limit_mult,
            overflow_hard_limit=overflow_hard_limit,
            enable_watchdog=enable_watchdog,
        )
        _IO.open()


def step(u: float, enable: int | float = 1) -> tuple[float, float, float, float, float, float, float, float]:
    """
    One tick. Returns (8 outputs, unchanged):
      theta, phi, theta_dot, phi_dot, current, fault, backlog, rt_ok
    """
    global _IO
    if _IO is None:
        start()

    assert _IO is not None

    en = bool(int(enable))
    s = _IO.step(
        motor_voltage=float(u),
        motor_enable=en,
        led_rgb=(False, True, False) if en else (True, False, False),
    )

    return (
        float(s.theta),
        float(s.phi),
        float(s.theta_dot),
        float(s.phi_dot),
        float(s.current),
        float(s.fault),
        float(s.backlog),
        float(s.rt_ok),
    )


def step_mon(
    u: float,
    enable: int | float = 1,
) -> tuple[
    float, float, float, float, float, float, float, float,
    float, float, float, float
]:
    """
    One tick with monitoring (12 outputs):
      theta, phi, theta_dot, phi_dot, current, fault, backlog, rt_ok,
      dt_wall, miss_count, overflow_delta, faulted

    Use this in Simulink if you want to wire monitoring outputs.
    """
    global _IO
    if _IO is None:
        start()

    assert _IO is not None

    en = bool(int(enable))
    s = _IO.step(
        motor_voltage=float(u),
        motor_enable=en,
        led_rgb=(False, True, False) if en else (True, False, False),
    )

    return (
        float(s.theta),
        float(s.phi),
        float(s.theta_dot),
        float(s.phi_dot),
        float(s.current),
        float(s.fault),
        float(s.backlog),
        float(s.rt_ok),

        float(s.dt_wall),
        float(s.miss_count),
        float(s.overflow_delta),
        float(1.0 if s.faulted else 0.0),
    )


def stop() -> None:
    global _IO
    if _IO is not None:
        try:
            # Safe output + red LED
            _IO.step(0.0, motor_enable=False, led_rgb=(True, False, False))
        except Exception:
            pass
        _IO.close()
        _IO = None
