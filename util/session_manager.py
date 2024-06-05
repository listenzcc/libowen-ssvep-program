"""
File: session_manager.py
Author: Chuncheng Zhang
Date: 2024-06-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

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
import numpy as np
import pandas as pd

from datetime import datetime
from pathlib import Path

from . import logger


# %% ---- 2024-06-04 ------------------------
# Function and class
def txt2df(txt: str) -> pd.DataFrame:
    rows = txt.split(";")
    rows = [[e.strip() for e in row.split(',')] for row in rows]
    columns = ['i', 'name', 'x', "y", "w", "h", 'omega', 'phi']
    df = pd.DataFrame(rows, columns=columns)
    for k in ['x', "y", "w", "h", 'omega', 'phi']:
        df[k] = df[k].map(float)
    return df


def df2txt(df: pd.DataFrame) -> str:
    values = df.values
    txt = ';\n'.join(','.join(f'{e}' for e in row) for row in values)
    return txt


class SessionManager(object):
    dfs = {}

    def __init__(self, root: Path):
        self.root = root
        root.mkdir(parents=True, exist_ok=True)
        self.refresh()
        logger.info(f'Initialized with {root}')

    def refresh(self):
        dfs = {
            e.name: pd.read_csv(e, index_col=None)
            for e in self.root.iterdir()
            if e.is_file() and e.name.endswith('.csv')}
        self.dfs = dfs
        logger.debug(f'Got sessions {len(dfs)}')
        return dfs

    def save(self, name: str, txt: str):
        name = name.strip()
        try:
            df = txt2df(txt)

            if not name:
                d = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
                name = f'{d}-{len(df)}-{random.random():0.8f}'
            if not name.endswith('.csv'):
                name += '.csv'

            df.to_csv(self.root.joinpath(name), index=False)

            logger.debug(f'Saved new session {name}')
        except Exception as e:
            logger.error(f'Failed to save session {name}: {e}')

    def get_by_name(self, name: str):
        name = name.strip()
        if not name.endswith('.csv'):
            name += '.csv'

        try:
            df = self.dfs[name]
            return df2txt(df)
        except Exception as e:
            logger.error(f'Failed to get {name}: {e}')


class TimeSeriesManager(object):
    def __init__(self, root: Path):
        self.root = root
        logger.info(f'Initialized with {root}')

    def get_by_name(self, name: str = 'ts') -> pd.DataFrame:
        if not name.endswith('.csv'):
            name += '.csv'
        path = self.root.joinpath(name)
        return pd.read_csv(path, index_col=0)

    def merge_with_txt(self, txt: str, body_length) -> pd.DataFrame:
        df1 = txt2df(txt)
        df2 = self.get_by_name()

        # How many points are required
        # Assume sampling interval is 0.01 seconds
        body_length = float(body_length)
        n = int(body_length / 0.01)
        seconds = np.array([i*0.01 for i in range(n)])

        dfs = []
        for _, se in df1.iterrows():
            name = se['name']
            if name in df2.columns:
                value = df2[name].to_numpy().squeeze()
                repeats = np.max([1, int(n/len(value)+1)])
                value = np.concatenate([value]*repeats)[:n]
                _df = pd.DataFrame()
                _df['value'] = value
                _df['type'] = 'ts'
            else:
                _df = pd.DataFrame()
                omega = float(se['omega'])
                phi = float(se['phi'])
                _df['value'] = np.cos(seconds*omega + phi) * 0.5 + 0.5
                _df['type'] = 'compute'

            _df['name'] = name
            _df['seconds'] = seconds
            dfs.append(_df)
        df = pd.concat(dfs)
        print(df)

        mat = df['value'].to_numpy().reshape((len(df) // n, n))
        corrcoef = np.corrcoef(mat)
        names = df1['name']
        df_corr = pd.DataFrame(np.abs(corrcoef), columns=names)
        df_corr.index = names

        print(df_corr)

        return df, df_corr


# %% ---- 2024-06-04 ------------------------
# Play ground


# %% ---- 2024-06-04 ------------------------
# Pending


# %% ---- 2024-06-04 ------------------------
# Pending
