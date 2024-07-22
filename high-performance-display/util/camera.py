"""
File: camera.py
Author: Chuncheng Zhang
Date: 2024-06-13
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Camera ready

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-06-13 ------------------------
# Requirements and constants
import cv2
import numpy as np

from PIL import Image
from threading import Thread
from . import logger


# %% ---- 2024-06-13 ------------------------
# Function and class
class CameraReady(object):
    cap = None
    width = 640
    height = 480
    mode = 'RGBA'
    patch = None
    camera_id = 0
    running = True

    def __init__(self, camera_id: int = 0):
        self.patch = self.empty_patch()
        self.camera_id = camera_id

    def empty_patch(self) -> Image:
        patch = Image.fromarray(np.random.randint(
            0, 256, (self.height, self.width, 3)), mode='RGB')
        return patch

    def start_capture_threads(self):
        Thread(target=self._link_capture, daemon=True).start()
        Thread(target=self._keep_capturing, daemon=True).start()

    def stop(self):
        if self.cap:
            self.cap.release()
        logger.info(f'Released camera: {self.cap}')

    def _link_capture(self):
        # It costs seconds to startup the camera
        self.cap = cv2.VideoCapture(self.camera_id)
        logger.info(f'Linked with camera: {self.cap}')

    def _keep_capturing(self):
        logger.info('Start capturing')
        while self.running:
            try:
                success, m = self.cap.read()
            except Exception as err:
                success = False

            if success:
                patch = Image.fromarray(
                    cv2.cvtColor(m[:, ::-1], cv2.COLOR_BGR2RGB))
            else:
                patch = self.empty_patch()

            self.patch = patch.convert(self.mode)
        logger.info('Stopped capturing')


# %% ---- 2024-06-13 ------------------------
# Play ground


# %% ---- 2024-06-13 ------------------------
# Pending


# %% ---- 2024-06-13 ------------------------
# Pending
