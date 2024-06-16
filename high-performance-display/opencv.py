"""
File: opencv.py
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
import time
import opensimplex

import numpy as np

from PIL import Image, ImageDraw
from util.timer import RunningTimer


# %% ---- 2024-06-13 ------------------------
# Function and class

opensimplex.seed(time.time_ns())


class Looping(object):
    running = True


width = 1920
height = 1080

# width = 800
# height = 600


def mk_rnd_image(width=width, height=height):
    img = Image.fromarray(np.random.randint(
        0, 255, [height, width, 4]) * 0 + 120, mode='RGBA')
    return img

# %% ---- 2024-06-13 ------------------------
# Play ground


img = mk_rnd_image()
img = Image.open(
    'C:\\Users\\zcc\\OneDrive\\Pictures\\DesktopPictures\\4kznds2.jpg').convert('RGBA').resize((width, height))
draw = ImageDraw.Draw(img)

winname = 'Main window'

rt = RunningTimer()
rt.reset()

looping = Looping()


def main_loop():
    passed = rt.get()
    rt.step()

    # _img = mk_rnd_image()
    _img = img.copy()

    # draw = ImageDraw.Draw(_img)
    x = int((opensimplex.noise2(x=0.1, y=passed)+1) * 0.5 * width)
    y = int((opensimplex.noise2(x=0.5, y=passed)+1) * 0.5 * height)

    for x in range(0, width, 100):
        for y in range(0, height, 100):
            c = int((opensimplex.noise3(x=x, y=y, z=passed)+1) * 0.5 * 255)
            draw.rectangle((x, y, x+50, y+50), fill=(c, c, c, 200))

    cv2.imshow(winname, cv2.cvtColor(
        np.array(img, dtype=np.uint8), cv2.COLOR_RGB2BGR))

    key_code = cv2.pollKey()
    if key_code > 0:
        print(key_code)
        if key_code == 27:
            looping.running = False
    time.sleep(0.0001)


cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while looping.running:
    main_loop()


# %% ---- 2024-06-13 ------------------------
# Pending


# %% ---- 2024-06-13 ------------------------
# Pending
