"""
File: tk.py
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
import time
import opensimplex
import numpy as np
import tkinter as tk

from threading import Thread
from PIL import ImageTk, Image, ImageDraw
from random import seed, choice
from string import ascii_letters

seed(42)

colors = ('red', 'yellow', 'green', 'cyan', 'blue', 'magenta')
colors = ('black', 'black')

opensimplex.seed(time.time_ns())


class Timer(object):
    tic = time.time()
    frames = 0
    passed = 0

    def step(self):
        self.frames += 1
        return self.frames

    def reset(self):
        self.tic = time.time()
        self.frames = 0
        self.passwd = 0
        self.passwd_max = 0

    def get(self):
        self.passed = time.time() - self.tic
        self.frame_rate = self.frames / self.passed
        return self.frame_rate, self.passed


timer = Timer()


def do_stuff():
    passed, frame_rate = timer.get()

    timer.step()

    rnd_string = [choice(ascii_letters) for i in range(10)]
    label_string = f'{frame_rate:0.4f}\t{passed:0.4f}\t{rnd_string}'
    color = choice(colors)
    tk_label.config(text=label_string, fg=color)

    _img = img.copy()
    draw = ImageDraw.Draw(_img)
    x = int((opensimplex.noise2(x=0.1, y=passed)+1) * 0.5 * size[0])
    y = int((opensimplex.noise2(x=0.5, y=passed)+1) * 0.5 * size[1])
    draw.rectangle((x, y, x+20, y+30), fill='red')
    photo_image.paste(_img)

    return passed

    # root.after(1, do_stuff)


root = tk.Tk()
root.wm_overrideredirect(True)
geometry = "{0}x{1}+0+0".format(root.winfo_screenwidth(),
                                root.winfo_screenheight())
root.geometry(geometry)
root.attributes('-alpha', 0.5)

r, g, b = root.winfo_rgb("white")


def on_key_press(evt):
    print(evt)


root.bind("<Escape>", lambda evt: root.destroy())
root.bind('<KeyPress>', lambda evt: on_key_press(evt))

# label = tk.Label(text='', font=("Helvetica", 60))
tk_label = tk.Label(text='', font=("Monospace", 20))

size = (1920, 1080)

img = Image.fromarray(np.random.randint(
    0, 255, [size[1], size[0], 3]), mode='RGB')
draw = ImageDraw.Draw(img)
photo_image = ImageTk.PhotoImage(image=img)
tk_label2 = tk.Label(image=photo_image)


tk_label.pack(expand=True)
tk_label2.pack(expand=True)
# tk_label2.place(x=100, y=100)


def loop():
    while True:
        print(do_stuff())

# do_stuff()


Thread(target=loop, daemon=True).start()

root.mainloop()


# %% ---- 2024-06-13 ------------------------
# Function and class


# %% ---- 2024-06-13 ------------------------
# Play ground


# %% ---- 2024-06-13 ------------------------
# Pending


# %% ---- 2024-06-13 ------------------------
# Pending
