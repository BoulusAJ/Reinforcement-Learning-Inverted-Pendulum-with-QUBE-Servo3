# Python/src/rl_qube/interface/qube3_pal_interface.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional, Any
import math
import numpy as np

from pal.products.qube import QubeServo3


def wrap_to_pi(x: float) -> float:
    return (x + math.pi) % (2.0 * math.pi) - math.pi


def to_float(x: Any) -> float:
    """
    PAL sometimes returns numpy scalars or 1-element arrays.
    Normalize to a Python float.
    """
    if isinstance(x, np.ndarray):
        if x.size == 1:
            return float(x.reshape(-1)[0])
        # If it’s an array unexpectedly, take first element (debug later)
        return float(x.reshape(-1)[0])
    return float(x)


@dataclass
class Qube3State:
    theta: float
    phi: float
    theta_dot: float
    phi_dot: float
    current: float
    fault: int
    stall_detect: int
    stall_error: int
    motor_counts: int
    pendulum_counts: int
    motor_cps: float
    pendulum_cps: float
    theta_unwrapped: float
    phi_unwrapped: float
    backlog: int
    rt_ok: bool

@dataclass
class Qube3State_1:
    theta: float
    phi: float
    theta_dot: float
    phi_dot: float
    current: float
    fault: int
    stall_detect: int
    stall_error: int
    motor_counts: int
    pendulum_counts: int
    motor_cps: float
    pendulum_cps: float
    theta_unwrapped: float
    phi_unwrapped: float

class Qube3PALInterface:
    """
    PAL-based QUBE-Servo 3 interface using task-based timing (readMode=1).
    Mimics a discrete Simulink-style step at a fixed frequency (e.g. 200 Hz).
    """

    def __init__(
        self,
        frequency: int = 200,
        motor_voltage_limit: float = 8.0,
        drop_old_samples: bool = True,
    ):
        self.frequency = int(frequency)
        self.dt = 1.0 / self.frequency
        self.motor_voltage_limit = float(motor_voltage_limit)
        self.drop_old_samples = bool(drop_old_samples)

        self._qube: Optional[QubeServo3] = None
        self._cm_entered: bool = False

        self._theta_prev = None
        self._theta_unwrapped = 0.0
        self._phi_prev = None
        self._phi_unwrapped = 0.0
        
        self.max_backlog_warn = 2
        self.max_backlog_flush = 3
        self.max_backlog_failsafe = 5

    def open(self) -> None:
        # Create object
        q = QubeServo3(
            hardware=1,
            pendulum=1,
            frequency=self.frequency,
            readMode=1,   # task-based timing
        )

        # Enter context manager explicitly (equivalent to: with QubeServo3(...) as q:)
        self._qube = q
        q.__enter__()
        self._cm_entered = True

        # Safe initial outputs
        q.write_voltage(0.0)
        q.write_led(np.array([0.0, 0.0, 0.0], dtype=np.float64))

    def close(self) -> None:
        if self._qube is None:
            return

        try:
            self._qube.write_voltage(0.0)
            # Red LED on stop (optional)
            self._qube.write_led(np.array([1.0, 0.0, 0.0], dtype=np.float64))
        except Exception:
            pass

        # Exit context manager if we entered it
        try:
            if self._cm_entered:
                self._qube.__exit__(None, None, None)
        finally:
            self._qube = None
            self._cm_entered = False

    @staticmethod
    def unwrap_step(prev: float | None, unwrapped: float, current: float) -> tuple[float, float]:
        if prev is None:
            return current, current
        d = current - prev
        # unwrap by nearest 2*pi multiple
        d = (d + math.pi) % (2*math.pi) - math.pi
        return current, unwrapped + d
    
    def step_1(
        self,
        motor_voltage: float,
        motor_enable: bool = True,
        led_rgb: Tuple[bool, bool, bool] = (False, True, False),
    ) -> Qube3State_1:
        if self._qube is None:
            raise RuntimeError("Qube3PALInterface not opened. Call open() first.")

        q = self._qube

        # --- Read (task timed) ---
        q.read_outputs()

        # Best-effort backlog drop (only if PAL exposes a counter)
        if self.drop_old_samples:
            samples_avail = getattr(q, "samplesAvailable", None)
            if samples_avail is None:
                samples_avail = getattr(q, "samples_available", None)
            if samples_avail is not None:
                try:
                    while int(samples_avail) > 1:
                        q.read_outputs()
                        # refresh
                        samples_avail = getattr(q, "samplesAvailable", samples_avail)
                        samples_avail = getattr(q, "samples_available", samples_avail)
                except Exception:
                    pass

        # Pull signals (names match Quanser examples)
        theta_u = to_float(getattr(q, "motorPosition"))
        phi_u = to_float(getattr(q, "pendulumPosition"))
        theta = wrap_to_pi(theta_u)
        phi = wrap_to_pi(phi_u)

        theta_dot = to_float(getattr(q, "motorSpeed"))
        phi_dot = to_float(getattr(q, "pendulumSpeed"))
        current = to_float(getattr(q, "motorCurrent"))

        self._theta_prev, self._theta_unwrapped = self.unwrap_step(self._theta_prev, self._theta_unwrapped, theta_u)
        self._phi_prev, self._phi_unwrapped = self.unwrap_step(self._phi_prev, self._phi_unwrapped, phi_u)


        # Fault flags: attribute names vary a bit; handle both
        fault = int(to_float(getattr(q, "motorFault", 0)))
        stall_detect = int(to_float(getattr(q, "stallDetected", 0)))
        stall_error = int(to_float(getattr(q, "stallError", 0)))

        # --- Write (actuation) ---
        v = float(motor_voltage)
        v = max(-self.motor_voltage_limit, min(self.motor_voltage_limit, v))
        if not motor_enable:
            v = 0.0

        q.write_voltage(v)

        r, g, b = led_rgb
        q.write_led(np.array([1.0 if r else 0.0, 1.0 if g else 0.0, 1.0 if b else 0.0], dtype=np.float64))

        motor_counts = int(to_float(getattr(q, "motorEncoderCounts")))
        pendulum_counts = int(to_float(getattr(q, "pendulumEncoderCounts")))
        motor_cps = to_float(getattr(q, "motorCountsPerSecond"))
        pendulum_cps = to_float(getattr(q, "pendulumCountsPerSecond"))

        return Qube3State_1(
            theta=theta,
            phi=phi,
            theta_dot=theta_dot,
            phi_dot=phi_dot,
            current=current,
            fault=fault,
            stall_detect=stall_detect,
            stall_error=stall_error,
            motor_counts=motor_counts,
            pendulum_counts=pendulum_counts,
            motor_cps=motor_cps,
            pendulum_cps=pendulum_cps,
            theta_unwrapped=self._theta_unwrapped,
            phi_unwrapped=self._phi_unwrapped
        )

    def step(
        self,
        motor_voltage: float,
        motor_enable: bool = True,
        led_rgb: Tuple[bool, bool, bool] = (False, True, False),
    ) -> Qube3State:
        if self._qube is None:
            raise RuntimeError("Qube3PALInterface not opened. Call open() first.")

        q = self._qube

        # --- Read (task timed) ---
        q.read_outputs()

        # --- Backlog / overrun handling (PAL task buffer) ---
        # PAL exposes:
        #   q.samplesToRead  -> how many samples we request per read (typically 1)
        #   q.samples        -> samples available/returned since last read (backlog indicator)
        #
        # Interpretation:
        #   backlog = max(0, samples - samplesToRead)
        #
        # Policy:
        #   backlog <= 1 : ok
        #   backlog == 2 : warn (late)
        #   backlog >= 3 : flush to latest (drop old)
        #   backlog >= 5 : fail-safe (disable motor this step)
        samples_to_read = int(getattr(q, "samplesToRead", 1) or 1)
        samples = int(getattr(q, "samples", samples_to_read) or samples_to_read)
        backlog = max(0, samples - samples_to_read)

        rt_ok = True
        failsafe_disable = False

        if self.drop_old_samples:
            # If backlog is large, flush to the newest sample
            if backlog >= self.max_backlog_flush:
                # How many extra samples are we behind by
                extra = backlog
                try:
                    # Read and discard extra samples, leaving us at most 0 backlog
                    # Note: q.read_outputs() reads samples_to_read each call.
                    # We loop until the reported backlog shrinks or we hit a cap.
                    flush_cap = 50  # avoid infinite loops if attribute doesn't update as expected
                    while extra > 0 and flush_cap > 0:
                        q.read_outputs()
                        flush_cap -= 1
                        samples = int(getattr(q, "samples", samples_to_read) or samples_to_read)
                        backlog = max(0, samples - samples_to_read)
                        extra = backlog
                except Exception:
                    # If flushing fails, we'll mark not OK and continue with latest we have
                    rt_ok = False

        # If still badly behind after flushing (or if we were very behind), fail safe
        if backlog >= self.max_backlog_failsafe:
            rt_ok = False
            failsafe_disable = True


        # Pull signals (names match Quanser examples)
        theta_u = to_float(getattr(q, "motorPosition"))
        phi_u = to_float(getattr(q, "pendulumPosition"))
        theta = wrap_to_pi(theta_u)
        phi = wrap_to_pi(phi_u)

        theta_dot = to_float(getattr(q, "motorSpeed"))
        phi_dot = to_float(getattr(q, "pendulumSpeed"))
        current = to_float(getattr(q, "motorCurrent"))

        self._theta_prev, self._theta_unwrapped = self.unwrap_step(self._theta_prev, self._theta_unwrapped, theta_u)
        self._phi_prev, self._phi_unwrapped = self.unwrap_step(self._phi_prev, self._phi_unwrapped, phi_u)


        # Fault flags: attribute names vary a bit; handle both
        fault = int(to_float(getattr(q, "motorFault", 0)))
        stall_detect = int(to_float(getattr(q, "stallDetected", 0)))
        stall_error = int(to_float(getattr(q, "stallError", 0)))

        # --- Write (actuation) ---
        v = float(motor_voltage)
        v = max(-self.motor_voltage_limit, min(self.motor_voltage_limit, v))
        if not motor_enable:
            v = 0.0
        if failsafe_disable:
            v = 0.0


        q.write_voltage(v)

        r, g, b = led_rgb
        q.write_led(np.array([1.0 if r else 0.0, 1.0 if g else 0.0, 1.0 if b else 0.0], dtype=np.float64))

        motor_counts = int(to_float(getattr(q, "motorEncoderCounts")))
        pendulum_counts = int(to_float(getattr(q, "pendulumEncoderCounts")))
        motor_cps = to_float(getattr(q, "motorCountsPerSecond"))
        pendulum_cps = to_float(getattr(q, "pendulumCountsPerSecond"))

        return Qube3State(
            theta=theta,
            phi=phi,
            theta_dot=theta_dot,
            phi_dot=phi_dot,
            current=current,
            fault=fault,
            stall_detect=stall_detect,
            stall_error=stall_error,
            motor_counts=motor_counts,
            pendulum_counts=pendulum_counts,
            motor_cps=motor_cps,
            pendulum_cps=pendulum_cps,
            theta_unwrapped=self._theta_unwrapped,
            phi_unwrapped=self._phi_unwrapped,
            backlog=backlog,
            rt_ok=rt_ok,
        )
    


