"""
File: websocket_client.py
Author: Chuncheng Zhang
Date: 2024-06-06
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


# %% ---- 2024-06-06 ------------------------
# Requirements and constants
from websockets.sync.client import connect

from . import logger


# %% ---- 2024-06-06 ------------------------
# Function and class

class MyWebsocketClient(object):
    url = 'ws://localhost:23335'

    def send(self, pkg):
        with connect(self.url, max_size=3000000) as websocket:
            websocket.send(pkg)
            logger.debug(f'Sent {pkg[:20]}, {len(pkg)}')
            received = websocket.recv()
            logger.debug(f'Received {received[:20]}, {len(pkg)}')
            return received


# %% ---- 2024-06-06 ------------------------
# Play ground


# %% ---- 2024-06-06 ------------------------
# Pending


# %% ---- 2024-06-06 ------------------------
# Pending
