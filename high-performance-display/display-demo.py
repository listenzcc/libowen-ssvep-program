"""
File: display-demo.py
Author: Chuncheng Zhang
Date: 2024-07-25
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    A demo of using the util/display_engine.py

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-07-25 ------------------------
# Requirements and constants
import sys

from PyQt6.QtCore import Qt, QTimer

from util import logger
from util.timer import RunningTimer
from util.camera import CameraReady
from util.display_engine import DisplayEngine

# Set DisplayEngine
de = DisplayEngine()

# Set running timer
tr = RunningTimer('Frontend')

# Set CameraReady
cr = CameraReady(width=de.width//4, height=de.height//6)
cr.start_capture_threads()


# %% ---- 2024-07-25 ------------------------
# Function and class


def _about_to_quit():
    '''
    Safely quit the demo
    '''
    de.stop()
    logger.debug('Stopped DisplayEngine')

    cr.stop()
    logger.debug('Stopped CameraReady')
    return


def _on_key_pressed(event):
    '''
    Handle the key pressed event.

    Args:
        - event: The pressed event.
    '''

    try:
        key = event.key()
        enum = Qt.Key(key)
        logger.debug(f'Key pressed: {key}, {enum.name}')
        if enum.name == 'Key_Escape':
            de.app.quit()
    except Exception as err:
        logger.error(f'Key pressed but I got an error: {err}')


# Bind the runtime functions
de.app.aboutToQuit.connect(_about_to_quit)
de.window.keyPressEvent = _on_key_pressed

# %% ---- 2024-07-25 ------------------------
# Play ground
if __name__ == '__main__':
    # Show the window
    de.window.show()

    tr.reset()

    def _on_timeout():
        tr.step()
        img = de.img.copy()
        img.paste(cr.patch)
        de.repaint(img)

    timer = QTimer()
    timer.timeout.connect(_on_timeout)
    timer.start()

    # Start the display main loop
    de.start()

    # Execute the app
    sys.exit(de.app.exec())


# %% ---- 2024-07-25 ------------------------
# Pending


# %% ---- 2024-07-25 ------------------------
# Pending
