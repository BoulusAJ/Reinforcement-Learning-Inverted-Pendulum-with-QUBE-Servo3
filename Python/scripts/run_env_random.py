# Python/scripts/run_env_random.py

import time
import numpy as np
from rl_qube.envs.qube_balance_env import QubeBalanceEnv

env = QubeBalanceEnv()

obs = env.reset()
print("Env reset. Running random actions…")

try:
    for k in range(2000):  # 10 seconds
        action = 0.3 * np.random.randn()  # very small
        obs, reward, done, info = env.step(action)

        if k % 100 == 0:
            print(
                f"k={k:04d} "
                f"phi={info['phi']:+.3f} "
                f"reward={reward:+.3f}"
            )

        if done:
            print("Episode terminated:", info)
            break

        time.sleep(env.Ts)

finally:
    env.close()
    print("Stopped safely.")

