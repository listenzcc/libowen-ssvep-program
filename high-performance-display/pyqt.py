"""
File: pyqt.py
Author: Chuncheng Zhang
Date: 2024-06-13
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


# %% ---- 2024-06-13 ------------------------
# Requirements and constants
import cv2
import sys
import opensimplex
import numpy as np
import time

from threading import Thread
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

from util.timer import RunningTimer
from util.camera import CameraReady


# %% ---- 2024-06-13 ------------------------
# Function and class
rt = RunningTimer()
cr = CameraReady()
cr.start_capture_threads()


class DisplayOption(object):
    flag_focus = True


do = DisplayOption()

# %% ---- 2024-06-13 ------------------------
# Play ground
app = QApplication(sys.argv)

window = QMainWindow()

# Translucent image by its RGBA A channel
window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
# Disable frame and keep the window on the top layer
# It is necessary to set the FramelessWindowHint for the WA_TranslucentBackground works
window.setWindowFlags(
    Qt.WindowType.FramelessWindowHint |
    Qt.WindowType.WindowStaysOnTopHint)
# Only hide window frame
# window.setWindowFlags(Qt.WindowType.FramelessWindowHint)

screen = app.primaryScreen()
width = screen.size().width() // 2
height = screen.size().height()

window.move(width, 0)

label = QLabel(window)

img = Image.open('image.jpg').resize((width, height)).convert('RGBA')
# img = Image.fromarray(
#     np.zeros((width, height, 4), dtype=np.uint8)).convert('RGBA')
draw = ImageDraw.Draw(img)
pixmap = QPixmap.fromImage(ImageQt(img))
# pixmap = QPixmap('po.png')

label.setPixmap(pixmap)
label.setGeometry(0, 0, pixmap.width(), pixmap.height())

window.label = label

window.resize(pixmap.width(), pixmap.height())

# window.showFullScreen()
window.show()


def about_to_quit():
    rt.running = False
    print(f'About to quit')
    # Make sure other processes receive the running signal down
    time.sleep(0.1)
    cr.stop()
    time.sleep(0.1)
    return


app.aboutToQuit.connect(about_to_quit)


def focus_changed(e):
    do.flag_focus = e is not None
    print(e, do.flag_focus)


app.focusWindowChanged.connect(focus_changed)


def key_pressed(evt):
    '''
    The key is int
    The enum is the enum of the key int code
    Either value and name is useful
    '''

    try:
        key = evt.key()
        enum = Qt.Key(key)
        print(f'Key pressed: {key}, {enum.name}')
        if enum.name == 'Key_Escape':
            app.quit()
    except Exception as err:
        print(f'Key pressed but I got an error: {err}')


window.keyPressEvent = key_pressed


def animating_loop():
    rt.reset()

    while rt.running:
        # Update the timer to the next frame
        rt.step()

        # Get the current time
        passed = rt.get()

        # Draw patches in the m x n grid
        # it follows the variable of passed
        patch_size = 200
        patch_gap = 250
        speed_factor = 10
        for x in range(0, width, patch_gap):
            for y in range(0, height, patch_gap):
                c = int(
                    (opensimplex.noise3(x=x, y=y, z=passed * speed_factor)+1) * 0.5 * 256)
                draw.rectangle(
                    (x, y, x+patch_size, y+patch_size), fill=(c, c, c, c))

        # Blink on the right top corner if not focused
        if not do.flag_focus:
            c = tuple(np.random.randint(0, 256, 3))
            draw.rectangle((width-50, 0, width, 50), fill=c)

        # Paste the Camera patch to the left top corner
        img.paste(cr.patch)

        # Convert the img into pixmap and display
        pixmap = QPixmap.fromImage(ImageQt(img))
        label.setPixmap(pixmap)
        time.sleep(0.001)

    print('Stopped animating loop')


Thread(target=animating_loop, daemon=True).start()

# sys.exit(app.exec())
app.exec()

# %% ---- 2024-06-13 ------------------------
# Pending


# %% ---- 2024-06-13 ------------------------
# Pending
