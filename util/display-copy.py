"""
File: display.py
Author: Chuncheng Zhang
Date: 2024-06-05
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Display with psychopy

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-06-05 ------------------------
# Requirements and constants
import time
import random
import numpy as np

from PIL import Image, ImageDraw

from psychopy import visual, core, event
from psychopy.hardware import keyboard

from . import logger


# %% ---- 2024-06-05 ------------------------
# Function and class
def random_color():
    rgb = [random.randint(0, 256) for _ in range(3)]
    return '#' + ''.join(hex(e).replace('x', '')[-2:] for e in rgb)


def color_by_float(t):
    rgb = [int(t*255) for _ in range(3)]
    return '#' + ''.join(hex(e).replace('x', '')[-2:] for e in rgb)


class MainWindow(object):
    tic = time.time()
    frame_count = 0
    debug = True

    def __init__(self, resolution_x=800, resolution_y=600, repeats=None, cue=None, df_layout=None, df_ts=None, head_length=None, body_length=None, tail_length=None):
        size = (resolution_x, resolution_y)
        win = visual.Window(size, monitor="textMonitor", units='pix')
        win.winHandle.activate()

        img = Image.fromarray(np.zeros((resolution_y, resolution_x)))
        draw = ImageDraw.Draw(img)
        self.img = img
        self.draw = draw
        print(img)

        img_full_screen = visual.ImageStim(win=win, image=img)
        img_full_screen.autoDraw = True
        self.img_full_screen = img_full_screen

        # Put the timer on the top center
        timer_msg = visual.TextStim(
            win=win, text='--:--:--', pos=[0, resolution_y/2 - 20])
        # Put the pnt on the north-east corner
        pnt = visual.GratingStim(
            win=win, size=10, pos=[resolution_x/2-10, resolution_y/2-10], sf=0)

        if self.debug:
            timer_msg.autoDraw = True
            pnt.autoDraw = True

        # --------------------
        self.size = size
        self.win = win
        self.timer_msg = timer_msg
        self.pnt = pnt

        # --------------------
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        self.repeats = repeats
        self.cue = cue
        self.df_layout = df_layout
        self.df_ts = df_ts
        self.head_length = head_length
        self.body_length = body_length
        self.tail_length = tail_length
        self.trial_length = head_length + body_length + tail_length

        self.mk_patches()

    def mk_patches(self):
        # --------------------
        patches = {}
        ts_objs = {}
        names = []
        for i, se in self.df_layout.iterrows():
            name = se['name']
            xy = [
                se['x']-se['w']/2,
                se['y'] - se['h'] / 2,
                se['x']+se['w']/2,
                se['y'] + se['h']/2]
            dct = dict(se, xy=xy)
            patches[name] = dct
            ts_objs[name] = self.df_ts[
                self.df_ts['name'] == name]['value'].to_numpy()
            seconds = self.df_ts[
                self.df_ts['name'] == name]['seconds'].to_numpy()
            names.append(name)

        self.seconds = seconds
        self.ts_objs = ts_objs
        self.patches = patches

        # --------------------
        if self.cue == '!Random':
            trials_cue = random.choices(names, k=self.repeats)
        elif self.cue == '!NoCue':
            trials_cue = [None] * self.repeats
        else:
            trials_cue = [self.cue] * self.repeats

        self.trials_cue = trials_cue

        return patches, trials_cue

    def update_frame(self):
        passed = self._update_timer()
        t = passed % (self.trial_length)
        i = np.min([self.repeats-1, int(passed // self.trial_length)])

        state = 'head'
        if t > self.head_length:
            state = 'body'
        if t > self.head_length + self.body_length:
            state = 'tail'

        self.timer_msg.text += f' | {i+1} trial | {state}'

        if state == 'head':
            cue = self.trials_cue[i]
            for k, se in self.patches.items():
                xy = se['xy']
                if se['name'] == cue:
                    self.draw.rectangle(xy=xy, fill=255)
                else:
                    self.draw.rectangle(xy=xy, fill=100)
            self.img_full_screen.image = self.img

        if state == 'body':
            tt = t - self.head_length
            j = len(self.seconds[self.seconds < tt])
            for k, se in self.patches.items():
                try:
                    xy = se['xy']
                    x = self.ts_objs[k][j]
                    self.draw.rectangle(xy=xy, fill=int(x*255))
                except Exception:
                    pass
            self.img_full_screen.image = self.img

        if state == 'tail':
            for k, se in self.patches.items():
                xy = se['xy']
                self.draw.rectangle(xy=xy, fill=100)
            self.img_full_screen.image = self.img

        self._update_pnt_color()
        self.win.flip()
        return passed

    def _update_timer(self):
        passed = time.time() - self.tic
        self.frame_count += 1

        minutes = int(passed // 60)
        seconds = int((passed // 1) % 60)
        remain = int((passed % 1)*100)

        frame_rate = self.frame_count / np.max([passed, 0.1])

        self.timer_msg.text = f'{minutes}:{seconds:02d}:{remain:02d} | {frame_rate:0.2f}Hz'
        return passed

    def _update_pnt_color(self):
        self.pnt.color = random_color()

    def main_loop(self):
        total_length = self.repeats * \
            (self.head_length + self.body_length + self.tail_length)
        logger.debug(f'Starting fames with {total_length} seconds')
        self.tic = time.time()
        self.frame_count = 0
        while True:
            if self.update_frame() > total_length:
                break
        logger.debug(f'Finished fames with {total_length} seconds')
        self.win.close()
        core.quit()


# %% ---- 2024-06-05 ------------------------
# Play ground


# %% ---- 2024-06-05 ------------------------
# Pending


# %% ---- 2024-06-05 ------------------------
# Pending
