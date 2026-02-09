#Python/src/rl_qube/envs/qube_balance_env.py

import math
import time
import numpy as np

from rl_qube.interface import Qube3PALInterface


class QubeBalanceEnv:
    """
    Minimal balance-only environment (200 Hz).
    No Gym dependency yet — intentionally simple.
    """

    def __init__(
        self,
        frequency: int = 200,
        voltage_limit: float = 2.0,
        phi_max: float = math.radians(60),
    ):
        self.Ts = 1.0 / frequency
        self.phi_max = phi_max

        self.io = Qube3PALInterface(
            frequency=frequency,
            motor_voltage_limit=voltage_limit,
            drop_old_samples=True,
        )

        self._t = 0.0
        self._opened = False

    def reset(self):
        """
        Reset environment.
        User places pendulum near upright manually.
        """
        # Open hardware if not already open
        if not hasattr(self, "_opened") or not self._opened:
            self.io.open()
            self._opened = True

        self._t = 0.0

        # Disable motor briefly
        self.io.step(0.0, motor_enable=False, led_rgb=(1, 0, 0))
        time.sleep(0.2)

        # Read initial state
        s = self.io.step(0.0, motor_enable=False, led_rgb=(1, 1, 0))
        return self._obs_from_state(s)


    def step(self, action: float):
        """
        action ∈ [-1, 1]
        """
        action = float(np.clip(action, -1.0, 1.0))

        s = self.io.step(
            motor_voltage=action,
            motor_enable=True,
            led_rgb=(False, True, False),
        )

        self._t += self.Ts

        obs = self._obs_from_state(s)
        reward = self._reward(s)
        done = self._done(s)

        info = {
            "theta": s.theta,
            "phi": s.phi,
            "fault": s.fault,
            "stall": s.stall_error,
        }

        return obs, reward, done, info

    def close(self):
        self.io.close()

    # ---------------- helpers ----------------

    def _obs_from_state(self, s):
        return np.array(
            [
                math.sin(s.theta),
                math.cos(s.theta),
                math.sin(s.phi),
                math.cos(s.phi),
                s.theta_dot,
                s.phi_dot,
            ],
            dtype=np.float32,
        )

    def _reward(self, s):
        # balance-only shaping
        return (
            math.cos(s.phi)     # upright pendulum
            - 0.01 * s.theta_dot**2
            - 0.01 * s.phi_dot**2
        )

    def _done(self, s):
        if s.fault or s.stall_error:
            return True
        if abs(s.phi) > self.phi_max:
            return True
        return False
