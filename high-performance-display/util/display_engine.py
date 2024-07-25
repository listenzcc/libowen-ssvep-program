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
import numpy as np

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

from loguru import logger

from .timer import RunningTimer


# %% ---- 2024-07-24 ------------------------
# Function and class
_app = QApplication()


class DisplayEngine(object):
    '''
    SSVEP display engine
    '''

    # Generate app first
    app = _app

    # Components
    window = QMainWindow()
    pixmap_container = QLabel(window)
    rt = RunningTimer()

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
            img: Image object, default is None.
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
            img: Image object.
        '''
        self.pixmap = QPixmap.fromImage(ImageQt(img))
        return

    def start(self):
        # TODO: Start running_loop in a thread.
        pass

    def stop(self):
        '''Stop the running main loop'''
        self.rt.running = False

    def main_loop(self):
        '''
        Main loop for SSVEP display.
        '''
        self.rt.reset()

        while self.rt.running:
            # Update the timer to the next frame
            self.rt.step()
            pass


# %% ---- 2024-07-24 ------------------------
# Play ground


# %% ---- 2024-07-24 ------------------------
# Pending


# %% ---- 2024-07-24 ------------------------
# Pending
