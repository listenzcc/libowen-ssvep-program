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
    return pd.DataFrame(rows, columns=columns)


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

            if len(name) == 0:
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


# %% ---- 2024-06-04 ------------------------
# Play ground


# %% ---- 2024-06-04 ------------------------
# Pending


# %% ---- 2024-06-04 ------------------------
# Pending
