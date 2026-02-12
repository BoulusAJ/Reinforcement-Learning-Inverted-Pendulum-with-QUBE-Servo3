# Python/src/rl_qube/interface/qube3_pal_interface.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Optional, Any
import math
import numpy as np
import time

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

    # Monitoring / safety telemetry (determinism supervision)
    dt_wall: float = 0.0
    miss_count: int = 0
    overflow_delta: int = 0
    faulted: bool = False


class Qube3PALInterface:
    """
    PAL-based QUBE-Servo 3 interface using task-based timing (readMode=1).
    Mimics a discrete Simulink-style step at a fixed frequency (e.g. 200 Hz).

    Determinism supervision:
      - dt_wall measured from perf_counter_ns
      - buffer overflows detected via task_get_buffer_overflows(readTask)
      - latched fault: keep returning safe outputs (0V) once faulted
      - optional hardware watchdog (best-effort)
    """

    def __init__(
        self,
        frequency: int = 200,
        motor_voltage_limit: float = 8.0,
        drop_old_samples: bool = True,  # kept for compatibility; no longer used for overwrite-mode backlog
        *,
        dt_hard_limit_mult: float = 10.0,   # hard-limit = mult * Ts
        overflow_hard_limit: int = 5,       # allow N overflows total before latch
        enable_watchdog: bool = True,
    ):
        self.frequency = int(frequency)
        self.dt = 1.0 / self.frequency
        self.motor_voltage_limit = float(motor_voltage_limit)
        self.drop_old_samples = bool(drop_old_samples)

        # Determinism / safety monitoring configuration
        self.dt_hard_limit_mult = float(dt_hard_limit_mult)
        self.overflow_hard_limit = int(overflow_hard_limit)
        self.enable_watchdog = bool(enable_watchdog)

        # Runtime monitoring state (initialized in open() / first step)
        self._last_step_t_ns: Optional[int] = None
        self._miss_count: int = 0
        self._faulted: bool = False

        self._overflow_total: int = 0
        self._last_overflows: Optional[int] = None

        self._watchdog_started: bool = False

        self._qube: Optional[QubeServo3] = None
        self._cm_entered: bool = False

        self._theta_prev: Optional[float] = None
        self._theta_unwrapped: float = 0.0
        self._phi_prev: Optional[float] = None
        self._phi_unwrapped: float = 0.0

    def open(self) -> None:
        # Create object
        q = QubeServo3(
            hardware=1,
            pendulum=1,
            frequency=self.frequency,
            readMode=1,   # task-based timing
        )

        # Enter context manager explicitly
        self._qube = q
        q.__enter__()
        self._cm_entered = True

        # Reset monitoring state
        self._last_step_t_ns = None
        self._miss_count = 0
        self._faulted = False
        self._overflow_total = 0
        self._last_overflows = None
        self._watchdog_started = False

        # Baseline overflow counter (best-effort)
        try:
            read_task = getattr(q, "_readTask", None)
            card = getattr(q, "card", None)
            if card is not None and read_task is not None:
                self._last_overflows = int(card.task_get_buffer_overflows(read_task))
        except Exception:
            self._last_overflows = None

        # Safe initial outputs
        try:
            q.write_voltage(0.0)
            q.write_led(np.array([0.0, 0.0, 0.0], dtype=np.float64))
        except Exception:
            pass

        # Optional hardware watchdog (best-effort; do not crash if unsupported)
        if self.enable_watchdog:
            try:
                card = getattr(q, "card", None)
                if card is not None:
                    timeout_s = float(self.dt_hard_limit_mult) * float(self.dt)

                    # Best-effort stop in case it's already running/expired
                    try:
                        card.watchdog_stop()
                    except Exception:
                        pass

                    # Configure analog expiration state to 0V on the write channels
                    try:
                        chans_raw = getattr(q, "WRITE_ANALOG_CHANNELS", None)
                        if chans_raw is not None:
                            chans = np.asarray(chans_raw, dtype=np.uint32).reshape(-1)
                            if chans.size > 0:
                                voltages = np.zeros(chans.size, dtype=np.float64)
                                card.watchdog_set_analog_expiration_state(chans, int(chans.size), voltages)
                    except Exception as e:
                        # Leave watchdog running without analog expiration if not supported
                        print("watchdog_set_analog_expiration_state failed:", e)

                    # Start + immediately reload once (kick)
                    print(timeout_s)
                    card.watchdog_start(float(timeout_s))
                    time.sleep(0.01)
                    is_watchdog_expired = card.watchdog_is_expired()
                    print("is_watchdog_expired_00:", is_watchdog_expired)
                    for i in range(5):
                        time.sleep(1)
                        is_watchdog_expired = card.watchdog_is_expired()
                        print("is_watchdog_expired_0:", is_watchdog_expired)
                        if is_watchdog_expired:
                            break        
                    try:
                        is_watchdog_expired = card.watchdog_is_expired()
                        print("is_watchdog_expired_1:", is_watchdog_expired)
                        print("watchdog_reload status:", card.watchdog_reload())
                        is_watchdog_expired = card.watchdog_is_expired()
                        print("is_watchdog_expired_2:", is_watchdog_expired)
                    except Exception as e:
                        print(e)
                        pass

                    self._watchdog_started = True

            except Exception as e:
                print("watchdog init failed:", e)
                self._watchdog_started = False


    def close(self) -> None:
        if self._qube is None:
            return

        q = self._qube

        # Try to stop watchdog first (avoid leaving device in watchdog mode)
        try:
            if self._watchdog_started:
                card = getattr(q, "card", None)
                if card is not None:
                    card.watchdog_stop()
        except Exception:
            pass
        finally:
            self._watchdog_started = False

        # Force safe outputs
        try:
            q.write_voltage(0.0)
            # Red LED on stop (optional)
            q.write_led(np.array([1.0, 0.0, 0.0], dtype=np.float64))
        except Exception:
            pass

        # Exit context manager if we entered it
        try:
            if self._cm_entered:
                q.__exit__(None, None, None)
        finally:
            self._qube = None
            self._cm_entered = False

    @staticmethod
    def unwrap_step(prev: float | None, unwrapped: float, current: float) -> tuple[float, float]:
        if prev is None:
            return current, current
        d = current - prev
        d = (d + math.pi) % (2 * math.pi) - math.pi
        return current, unwrapped + d

    def _watchdog_reload_best_effort(self) -> bool:
        """
        Reload watchdog. Returns True if reload succeeded, False otherwise.
        We DO NOT latch based solely on watchdog_is_expired() because some drivers
        report it sticky/latched. We latch on reload failure instead.
        """
        if not (self.enable_watchdog and self._watchdog_started):
            return True  # watchdog not in use

        q = self._qube
        if q is None:
            return False

        try:
            card = getattr(q, "card", None)
            if card is None:
                return False

            card.watchdog_reload()
            return True
        except Exception:
            return False



    def step(
        self,
        motor_voltage: float,
        motor_enable: bool = True,
        led_rgb: Tuple[bool, bool, bool] = (False, True, False),
    ) -> Qube3State:
        if self._qube is None:
            raise RuntimeError("Qube3PALInterface not opened. Call open() first.")

        q = self._qube

        # --- Timing supervision (wall-clock) ---
        now_ns = time.perf_counter_ns()
        if self._last_step_t_ns is None:
            dt_wall = float(self.dt)
        else:
            dt_wall = (now_ns - self._last_step_t_ns) * 1e-9
        self._last_step_t_ns = now_ns

        dt_hard_limit = float(self.dt_hard_limit_mult) * float(self.dt)

        # Latch if we missed hard timing constraint
        if dt_wall > dt_hard_limit:
            self._miss_count += 1
            self._faulted = True

        # --- Reload watchdog EARLY (before doing I/O) ---
        # If reload fails, latch fault immediately.
        if not self._watchdog_reload_best_effort():
            self._faulted = True

        # --- Read (task timed) ---
        try:
            q.read_outputs()
        except Exception:
            self._faulted = True

        # --- Task buffer overflow monitoring (recommended for OVERWRITE_ON_OVERFLOW) ---
        overflow_delta = 0
        try:
            read_task = getattr(q, "_readTask", None)
            card = getattr(q, "card", None)
            if card is not None and read_task is not None:
                cur_overflows = int(card.task_get_buffer_overflows(read_task))
                if self._last_overflows is not None:
                    overflow_delta = max(0, cur_overflows - self._last_overflows)
                self._last_overflows = cur_overflows
        except Exception:
            overflow_delta = 0  # keep running; don't fault just for missing telemetry

        if overflow_delta > 0:
            self._overflow_total += int(overflow_delta)
            if self._overflow_total > self.overflow_hard_limit:
                self._faulted = True

        # backlog output now represents cumulative overflow count (as you intended)
        backlog = int(self._overflow_total)

        # --- Pull signals ---
        theta_u = to_float(getattr(q, "motorPosition", 0.0))
        phi_u = to_float(getattr(q, "pendulumPosition", 0.0))
        theta = wrap_to_pi(theta_u)
        phi = wrap_to_pi(phi_u)

        theta_dot = to_float(getattr(q, "motorSpeed", 0.0))
        phi_dot = to_float(getattr(q, "pendulumSpeed", 0.0))
        current = to_float(getattr(q, "motorCurrent", 0.0))

        self._theta_prev, self._theta_unwrapped = self.unwrap_step(
            self._theta_prev, self._theta_unwrapped, theta_u
        )
        self._phi_prev, self._phi_unwrapped = self.unwrap_step(
            self._phi_prev, self._phi_unwrapped, phi_u
        )

        motor_fault = int(to_float(getattr(q, "motorFault", 0)))
        stall_detect = int(to_float(getattr(q, "stallDetected", 0)))
        stall_error = int(to_float(getattr(q, "stallError", 0)))

        # Latch if hardware reports motor fault
        if motor_fault != 0:
            self._faulted = True

        # --- Fault action: latch + keep returning safe outputs (0V) ---
        v = float(motor_voltage)
        v = max(-self.motor_voltage_limit, min(self.motor_voltage_limit, v))

        if not motor_enable:
            v = 0.0

        if self._faulted:
            v = 0.0
            motor_enable = False

        # --- Write (actuation) ---
        try:
            q.write_voltage(v)
        except Exception:
            self._faulted = True
            try:
                q.write_voltage(0.0)
            except Exception:
                pass

        # LED: red on fault
        try:
            if self._faulted:
                rgb = (True, False, False)
            else:
                rgb = led_rgb
            r, g, b = rgb
            q.write_led(np.array([1.0 if r else 0.0,
                                1.0 if g else 0.0,
                                1.0 if b else 0.0], dtype=np.float64))
        except Exception:
            pass

        motor_counts = int(to_float(getattr(q, "motorEncoderCounts", 0)))
        pendulum_counts = int(to_float(getattr(q, "pendulumEncoderCounts", 0)))
        motor_cps = to_float(getattr(q, "motorCountsPerSecond", 0.0))
        pendulum_cps = to_float(getattr(q, "pendulumCountsPerSecond", 0.0))

        # "rt_ok" should mean "no latched fault"
        rt_ok = (not self._faulted)

        fault_out = int(self._faulted or (motor_fault != 0))

        return Qube3State(
            theta=theta,
            phi=phi,
            theta_dot=theta_dot,
            phi_dot=phi_dot,
            current=current,
            fault=fault_out,
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

            dt_wall=float(dt_wall),
            miss_count=int(self._miss_count),
            overflow_delta=int(overflow_delta),
            faulted=bool(self._faulted),
        )
