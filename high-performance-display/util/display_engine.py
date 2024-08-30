"""
File: display_engine.py
Author: Chuncheng Zhang
Date: 2024-07-24
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Display engine

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-07-24 ------------------------
# Requirements and constants
import sys
import time
import opensimplex
import numpy as np

from threading import Thread
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

from . import logger
from .timer import RunningTimer


# %% ---- 2024-07-24 ------------------------
# Function and class
_app = QApplication(sys.argv)


class DisplayEngine(object):
    '''
    SSVEP display engine
    '''

    # Generate app first
    app = _app

    # Components
    window = QMainWindow()
    pixmap_container = QLabel(window)
    rt = RunningTimer('BackendTimer')

    # Parameters in waiting
    width: int = None
    height: int = None
    img: Image = None
    img_drawer: ImageDraw = None
    pixmap: QPixmap = None

    # Options
    flag_has_focus: bool = True

    def __init__(self):
        '''
        Initialize by default
        '''
        self.prepare_window()
        self.prepare_img()
        self._handle_focus_change()
        logger.info('Initialized engine')

    def _handle_focus_change(self):
        '''
        Handle the focus change event.
        '''
        def focus_changed(e):
            self.flag_has_focus = e is not None
            logger.debug(f'Focus changed to {self.flag_has_focus}')
        self.app.focusWindowChanged.connect(focus_changed)
        logger.debug(f'Handled focus changed with {focus_changed}')
        return

    def show(self):
        '''
        Show the window
        '''
        self.window.show()
        logger.debug('Shown window')
        return

    def prepare_window(self):
        '''
        Prepare the window,
        - Set its size, position and transparency.
        - Set the self.pixmap_container geometry accordingly.
        '''
        # Translucent image by its RGBA A channel
        self.window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Disable frame and keep the window on the top layer
        # It is necessary to set the FramelessWindowHint for the WA_TranslucentBackground works
        self.window.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint)
        # Only hide window frame
        # self.window.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Fetch the screen size and set the size for the window
        screen = self.app.primaryScreen()
        self.width = screen.size().width() // 2
        self.height = screen.size().height()

        # Set the window size
        self.window.resize(self.width, self.height)

        # Put the window to the right
        self.window.move(self.width, 0)

        # Set the pixmap_container accordingly,
        # and it is within the window bounds
        self.pixmap_container.setGeometry(0, 0, self.width, self.height)

        logger.debug(
            f'Reset window size to {self.width}, {self.width}, and reset other stuff')
        return

    def prepare_img(self):
        '''
        Prepare the img and its relating,
        - Set the img object, its size and drawer.
        - Repaint with it for startup.
        '''
        # Generate fully transparent image and its drawer
        self.img = Image.fromarray(
            np.zeros((self.width, self.height, 4), dtype=np.uint8)).convert('RGBA')
        self.img_drawer = ImageDraw.Draw(self.img)

        # Repaint with default img for startup
        self.repaint()

        logger.debug(f'Prepared img, {self.img}, {self.img_drawer}')
        return

    def repaint(self, img: Image = None):
        '''
        Repaint with the given img.
        If it is None, using self.img as default.

        The pipeline is
        img -> pixmap -> pixmap_container

        Args:
            - img: Image object, default is None.
        '''

        # Use self.img if nothing is provided
        if img is None:
            img = self.img

        # img -> pixmap
        self.remake_pixmap(img)

        # pixmap -> pixmap_container
        self.pixmap_container.setPixmap(self.pixmap)

        return

    def remake_pixmap(self, img: Image = None):
        '''
        Remake the self.pixmap with the input img.

        Args:
            - img: Image object.
        '''
        self.pixmap = QPixmap.fromImage(ImageQt(img))
        return

    def start(self):
        ''' Start the main_loop '''
        Thread(target=self.main_loop, daemon=True).start()
        return

    def stop(self):
        ''' Stop the running main loop '''
        self.rt.running = False

    def main_loop(self):
        ''' Main loop for SSVEP display. '''
        self.rt.reset()

        logger.debug('Starting')
        while self.rt.running:
            # Update the timer to the next frame
            self.rt.step()

            # Get the current time
            passed = self.rt.get()

            # Draw the patches in the grid
            # The patch_gap should be larger than patch_size
            patch_size = 200
            patch_gap = 250
            # The flipping rate is faster when the speed_factor is faster
            speed_factor = 10
            z = passed * speed_factor
            # The two-loops generate x, y coordinates for the grid patches
            for x in range(0, self.width, patch_gap):
                for y in range(0, self.height, patch_gap):
                    # Generate continue noise,
                    # and linearly convert from (-1, 1) to (0, 1)
                    f = (opensimplex.noise3(x=x, y=y, z=z)+1) * 0.5
                    # Convert to [0, 255]
                    c = int(f * 256)
                    self.img_drawer.rectangle(
                        (x, y, x+patch_size, y+patch_size), fill=(c, c, c, c))

            # Blink on the right top corner in 50x50 pixels size if not focused
            if not self.flag_has_focus:
                c = tuple(np.random.randint(0, 256, 3))
                self.img_drawer.rectangle(
                    (self.width-50, 0, self.width, 50), fill=c)

            # Paint
            self._on_paint_subsystem()
            # self.repaint()

            # Continue after sleep
            time.sleep(0.001)
            pass
        logger.debug('Stopped')
        return

    def _on_paint_subsystem(self):
        '''Subsystem requires rewrite'''
        return


# %% ---- 2024-07-24 ------------------------
# Play ground


# %% ---- 2024-07-24 ------------------------
# Pending


# %% ---- 2024-07-24 ------------------------
# Pending
