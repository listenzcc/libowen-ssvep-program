"""
File: mk_timeseries.py
Author: Chuncheng Zhang
Date: 2024-06-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Generate time series for SSVEP patches

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-06-04 ------------------------
# Requirements and constants
import time
import random
import perlin_noise

import numpy as np
import pandas as pd

from pathlib import Path


# %% ---- 2024-06-04 ------------------------
# Function and class
class Option:
    tmax = 10  # Seconds
    tmin = 0  # Seconds
    interval = 0.01  # Seconds


def generate_time_series(chs: int = 20):
    times = np.arange(Option.tmin, Option.tmax, Option.interval)
    n = len(times)
    df = pd.DataFrame()
    for ch in range(chs):
        name = f'p-{ch}'
        octaves = random.randint(100, 200)
        noise = perlin_noise.PerlinNoise(octaves=octaves, seed=time.time())
        ts = np.array([noise(i/n) for i, times in enumerate(times)])*0.5 + 0.5
        ts -= np.min(ts)
        ts /= np.max(ts)
        df[name] = ts

    return df


# %% ---- 2024-06-04 ------------------------
# Play ground
if __name__ == "__main__":
    df = generate_time_series()
    path = Path(__file__).parent.joinpath('timeseries/ts.csv')
    df.to_csv(path)


# %% ---- 2024-06-04 ------------------------
# Pending


# %% ---- 2024-06-04 ------------------------
# Pending
