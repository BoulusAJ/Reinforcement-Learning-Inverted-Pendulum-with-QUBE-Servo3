from __future__ import annotations

from typing import Optional, Tuple
from rl_qube.interface.qube3_pal_interface import Qube3PALInterface

_IO: Optional[Qube3PALInterface] = None


def start(frequency: int = 200, vlimit: float = 2.0) -> None:
    global _IO
    if _IO is None:
        _IO = Qube3PALInterface(
            frequency=frequency,
            motor_voltage_limit=vlimit,
            drop_old_samples=True,
        )
        _IO.open()


def step(u: float, enable: int | float = 1) -> tuple[float, float, float, float, float, float]:
    """
    One tick. Returns:
    theta, phi, theta_dot, phi_dot, current, fault
    """
    global _IO
    if _IO is None:
        start()

    # At this point _IO is guaranteed not None, but Pylance may still not narrow across start().
    # So we re-assert explicitly:
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
    )


def stop() -> None:
    global _IO
    if _IO is not None:
        try:
            _IO.step(0.0, motor_enable=False, led_rgb=(True, False, False))
        except Exception:
            pass
        _IO.close()
        _IO = None
