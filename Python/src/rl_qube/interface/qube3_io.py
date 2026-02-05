# Interface/qube3_io.py
from __future__ import annotations
from dataclasses import dataclass
from array import array
from typing import Optional, Tuple

import math
import time


@dataclass
class Qube3Readout:
    enc0: int
    enc1: int
    theta: float   # rad (arm)
    phi: float     # rad (pendulum)
    status: int    # placeholder for now
    current: float # placeholder for now


class Qube3IO:
    """
    Minimal QUBE-Servo 3 I/O wrapper using Quanser SDK (no QUARC).

    This is designed to mirror the semantics of the Simulink 'raspi_Quanser' subsystem:
    - Write motor command (with enable)
    - Optional set encoder counts
    - Read encoders each step
    """

    def __init__(
        self,
        device: str = "qube_servo3_usb",
        device_id: str = "0",
        encoder_cpr: int = 2048,  # TODO confirm for your hardware
    ):
        self.device = device
        self.device_id = device_id
        self.encoder_cpr = encoder_cpr

        self._hil = None

        # Channels/buffers (Quanser API uses (channels, num_channels, buffer))
        self._ao_ch = array("I", [0])
        self._ao_n = len(self._ao_ch)
        self._ao_buf = array("d", [0.0])

        self._enc_ch = array("I", [0, 1])
        self._enc_n = len(self._enc_ch)
        self._enc_buf = array("i", [0, 0])

    def open(self) -> None:
        from quanser.hardware import HIL
        self._hil = HIL()
        self._hil.open(self.device, self.device_id)

        # Start safe: ensure motor off
        self._ao_buf[0] = 0.0
        self._hil.write_analog(self._ao_ch, self._ao_n, self._ao_buf)

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
        # counts -> revolutions -> radians
        return (counts / self.encoder_cpr) * (2.0 * math.pi)

    def step(
        self,
        motor_voltage: float,
        motor_enable: bool = True,
        set_encoder0: Optional[int] = None,
        set_encoder1: Optional[int] = None,
        led_rgb: Optional[Tuple[bool, bool, bool]] = None,
    ) -> Qube3Readout:
        """
        Perform one I/O cycle: optional encoder set, motor write, encoder read.
        """
        if self._hil is None:
            raise RuntimeError("Qube3IO not opened. Call open() first.")

        # Optional: set encoders (we’ll enable once you confirm API call name exists in your install)
        # Many Quanser installs provide: set_encoder_counts(channels, num_channels, buffer)
        if (set_encoder0 is not None) or (set_encoder1 is not None):
            try:
                enc_set_buf = array("i", [
                    int(set_encoder0 or 0),
                    int(set_encoder1 or 0),
                ])
                self._hil.set_encoder_counts(self._enc_ch, self._enc_n, enc_set_buf)
            except Exception:
                # If your SDK exposes a different method name, we’ll fix it after a quick introspection.
                pass

        # Motor command with enable gate
        v = float(motor_voltage) if motor_enable else 0.0
        self._ao_buf[0] = v
        self._hil.write_analog(self._ao_ch, self._ao_n, self._ao_buf)

        # Read encoders
        self._hil.read_encoder(self._enc_ch, self._enc_n, self._enc_buf)

        enc0 = int(self._enc_buf[0])
        enc1 = int(self._enc_buf[1])

        theta = self._counts_to_rad(enc0)
        phi = self._counts_to_rad(enc1)

        # Placeholders until we map them properly
        status = 0
        current = 0.0

        return Qube3Readout(enc0=enc0, enc1=enc1, theta=theta, phi=phi, status=status, current=current)
