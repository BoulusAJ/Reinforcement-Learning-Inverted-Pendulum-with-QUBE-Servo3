# Interface/qube3_io.py
from __future__ import annotations
from dataclasses import dataclass
from array import array
from typing import Optional, Tuple
import math
import time


@dataclass
class Qube3Readout:
    # Raw counts
    enc0: int
    enc1: int

    # Angles
    theta: float        # wrapped rad (-pi, pi]
    phi: float          # wrapped rad (-pi, pi]
    theta_unwrapped: float  # rad, continuous
    phi_unwrapped: float    # rad, continuous

    # Velocities (rad/s)
    theta_dot: float
    phi_dot: float

    # Diagnostics (placeholders until mapped)
    status: int
    current: float


def wrap_to_pi(x: float) -> float:
    # Wrap to (-pi, pi]
    return (x + math.pi) % (2.0 * math.pi) - math.pi


class Qube3IO:
    """
    QUBE-Servo 3 I/O wrapper using Quanser SDK (no QUARC).
    Designed to mirror the Simulink 'raspi_Quanser' semantics at a fixed sample time.

    Default dt=0.005 => 200 Hz, matching ts_raspi in the Servo2 project.
    """

    def __init__(
        self,
        device: str = "qube_servo3_usb",
        device_id: str = "0",
        dt: float = 0.005,
        encoder_cpr: int = 2048,
        motor_ao_channel: int = 0,
        enc0_channel: int = 0,
        enc1_channel: int = 1,
    ):
        self.device = device
        self.device_id = device_id
        self.dt = float(dt)
        self.encoder_cpr = int(encoder_cpr)

        self._hil = None

        # Analog out (motor voltage)
        self._ao_ch = array("I", [motor_ao_channel])
        self._ao_n = len(self._ao_ch)
        self._ao_buf = array("d", [0.0])

        # Encoders
        self._enc_ch = array("I", [enc0_channel, enc1_channel])
        self._enc_n = len(self._enc_ch)
        self._enc_buf = array("i", [0, 0])

        # State for finite-difference velocities
        self._prev_theta_unwrapped: Optional[float] = None
        self._prev_phi_unwrapped: Optional[float] = None
        self._prev_t: Optional[float] = None

    def open(self) -> None:
        from quanser.hardware import HIL
        self._hil = HIL()
        self._hil.open(self.device, self.device_id)

        # Start safe
        self._ao_buf[0] = 0.0
        self._hil.write_analog(self._ao_ch, self._ao_n, self._ao_buf)

        # Initialize velocity state with one read
        self._hil.read_encoder(self._enc_ch, self._enc_n, self._enc_buf)
        theta_u = self._counts_to_rad(int(self._enc_buf[0]))
        phi_u = self._counts_to_rad(int(self._enc_buf[1]))
        self._prev_theta_unwrapped = theta_u
        self._prev_phi_unwrapped = phi_u
        self._prev_t = time.perf_counter()

    def close(self) -> None:
        if self._hil is None:
            return
        try:
            self._ao_buf[0] = 0.0
            self._hil.write_analog(self._ao_ch, self._ao_n, self._ao_buf)
        except Exception:
            pass
        self._hil.close()
        self._hil = None

    def _counts_to_rad(self, counts: int) -> float:
        return (counts / self.encoder_cpr) * (2.0 * math.pi)

    def step(
        self,
        motor_voltage: float,
        motor_enable: bool = True,
        set_encoder0: Optional[int] = None,
        set_encoder1: Optional[int] = None,
        led_rgb: Optional[Tuple[bool, bool, bool]] = None,
    ) -> Qube3Readout:
        if self._hil is None:
            raise RuntimeError("Qube3IO not opened. Call open() first.")

        # Optional: set encoder counts (try; if method name differs, we’ll adjust)
        if (set_encoder0 is not None) or (set_encoder1 is not None):
            try:
                enc_set_buf = array("i", [
                    int(set_encoder0 or 0),
                    int(set_encoder1 or 0),
                ])
                self._hil.set_encoder_counts(self._enc_ch, self._enc_n, enc_set_buf)
            except Exception:
                # OK for now; not required for bring-up
                pass

        # Motor output (gate by enable)
        v = float(motor_voltage) if motor_enable else 0.0
        self._ao_buf[0] = v
        self._hil.write_analog(self._ao_ch, self._ao_n, self._ao_buf)

        # Read encoders
        self._hil.read_encoder(self._enc_ch, self._enc_n, self._enc_buf)
        enc0 = int(self._enc_buf[0])
        enc1 = int(self._enc_buf[1])

        theta_unwrapped = self._counts_to_rad(enc0)
        phi_unwrapped = self._counts_to_rad(enc1)

        theta = wrap_to_pi(theta_unwrapped)
        phi = wrap_to_pi(phi_unwrapped)

        # Velocities (finite difference; use fixed dt unless perf_counter is available)
        now = time.perf_counter()
        if self._prev_t is None:
            dt = self.dt
        else:
            dt = now - self._prev_t
            # If timing is weird, fall back to nominal dt
            if dt <= 0.0 or dt > 10.0 * self.dt:
                dt = self.dt

        if self._prev_theta_unwrapped is None or self._prev_phi_unwrapped is None:
            theta_dot = 0.0
            phi_dot = 0.0
        else:
            theta_dot = (theta_unwrapped - self._prev_theta_unwrapped) / dt
            phi_dot = (phi_unwrapped - self._prev_phi_unwrapped) / dt

        self._prev_theta_unwrapped = theta_unwrapped
        self._prev_phi_unwrapped = phi_unwrapped
        self._prev_t = now

        # Placeholders (we’ll map these next)
        status = 0
        current = 0.0

        return Qube3Readout(
            enc0=enc0,
            enc1=enc1,
            theta=theta,
            phi=phi,
            theta_unwrapped=theta_unwrapped,
            phi_unwrapped=phi_unwrapped,
            theta_dot=theta_dot,
            phi_dot=phi_dot,
            status=status,
            current=current
        )
