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
    # Predefined options
    camera_id = 0
    width = 640
    height = 480
    mode = 'RGBA'

    # Running time variables
    cap = None
    patch = None
    running = True

    def __init__(self, **kwargs):
        # Setup known options with arguments
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
                logger.debug(f'Set {k} to {v}')
            else:
                logger.warning(f'Invalid argument: {k}, {v}')

        # Initialize the patch
        self.patch = self.empty_patch()
        pass

    def empty_patch(self) -> Image:
        '''Make the empty patch with all-zero values'''
        patch = Image.fromarray(np.random.randint(
            0, 256, (self.height, self.width, 3)), mode='RGB')
        return patch

    def start_capture_threads(self):
        '''Start workload threads'''
        Thread(target=self._link_capture, daemon=True).start()
        Thread(target=self._keep_capturing, daemon=True).start()

    def stop(self):
        '''Stop the capture thread and release the resource'''
        if self.cap:
            self.cap.release()
        logger.info(f'Released camera: {self.cap}')

    def _link_capture(self):
        '''
        Links to the camera's capture service.
        It costs seconds to startup the camera.
        '''
        self.cap = cv2.VideoCapture(self.camera_id)
        logger.info(f'Linked with camera: {self.cap}')

    def _keep_capturing(self):
        '''Keep capturing the camera'''
        logger.info('Start capturing')
        while self.running:
            try:
                success, m = self.cap.read()
            except Exception as err:
                success = False

            if success:
                patch = Image.fromarray(cv2.cvtColor(
                    m[:, ::-1], cv2.COLOR_BGR2RGB)).resize((self.width, self.height))
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
