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
import base64
from io import BytesIO
import time
import random
import numpy as np

from enum import Enum
from threading import Thread
from PIL import Image, ImageDraw

from psychopy import visual, core, event
from psychopy.hardware import keyboard

import pickle
import websockets
import websockets.sync.server

from . import logger


# %% ---- 2024-06-05 ------------------------
# Function and class
kb = keyboard.Keyboard()


def random_color():
    rgb = [random.randint(0, 256) for _ in range(3)]
    return '#' + ''.join(hex(e).replace('x', '')[-2:] for e in rgb)


def color_by_float(t):
    rgb = [int(t*255) for _ in range(3)]
    return '#' + ''.join(hex(e).replace('x', '')[-2:] for e in rgb)


def convert_data_url_to_img(data_url):
    s = data_url.split('base64,', 1)[-1]
    decoded_bytes = base64.b64decode(s.replace('\\n', ''))
    img = Image.open(BytesIO(decoded_bytes))
    logger.debug(f'Converted {data_url[:20]} to {img}')
    return img


def gray2rgb(gray: int):
    return (gray, gray, gray)


class AvailableCurrentTasks(Enum):
    IDLE = 1
    SSVEP = 2


class MyWebsocketServer(object):
    host = 'localhost'
    port = 23335
    max_size = 300000000

    def __init__(self):
        self.serve_forever()

    def ws_echo(self, websocket):
        for message in websocket:
            logger.debug(f'Received {message[:20]}, {len(message)}')
            recovered = pickle.loads(message)

            if prompt := recovered.get('prompt'):
                self.osd_prompt_slogan_text = prompt
                logger.debug(f'Updated prompt: {prompt}')

            if recovered.get('task_name') == 'SSVEP':
                self.task_buffer.append(('SSVEP', recovered))
                logger.debug('Received SSVEP task')

            if recovered.get('task_name') == 'setUserProfile':
                profile = recovered.get(
                    'profile', dict(Error='Invalid user profile'))
                self.osd_user_profile_text = '\n'.join(
                    [f'{k}\t {v}' for k, v in profile.items()])
                logger.debug('Received setUserProfile task')

            if recovered.get('task_name') == 'checkoutDisplayStatus':
                msg = dict(
                    tasksInBuffer=len(self.task_buffer),
                    passed=self.passed,
                    total=self.total_length if hasattr(
                        self, 'total_length') else 'N.A.',
                    currentTask=self.current_task.name,
                    eventBuffer='\n'.join(
                        [f'{e}' for e in self.fifo_event_buffer.pop(0)]) if self.fifo_event_buffer else ''
                )
                pkg = pickle.dumps(msg)
                websocket.send(pkg)
                continue

            websocket.send('OK')

    def serve_forever(self):
        Thread(target=self._serve_forever, args=(), daemon=True).start()

    def _serve_forever(self):
        with websockets.sync.server.serve(self.ws_echo, self.host, self.port, max_size=self.max_size) as server:
            server.serve_forever()


class MainWindow(MyWebsocketServer):
    # Basic initialization
    resolution_x = 1920
    resolution_y = 1080
    win = visual.Window((resolution_x, resolution_y),
                        monitor='testMonitor', units='pix')

    # Put the OSD timer slogan on the top center
    osd_timer_slogan = visual.TextStim(
        win=win, text='--:--:--', pos=[0, resolution_y/2 - 20])
    # Put the blinking pnt on the north-east corner
    blinking_pnt = visual.GratingStim(
        win=win, size=10, pos=[resolution_x/2-10, resolution_y/2-10], sf=0)
    # Put the OSD slogan on the center
    osd_prompt_slogan_text = 'Welcome to my display text'
    osd_prompt_slogan = visual.TextStim(
        win=win, text=osd_prompt_slogan_text, pos=[0, 0])
    # Put the OSD user profile on the middle left
    osd_user_profile_text = 'Empty user profile'
    osd_user_profile = visual.TextStim(
        win=win, text=osd_user_profile_text, pos=[-resolution_x/2+20, 0], anchorHoriz='left'
    )

    # Task buffer
    task_buffer = []

    # Event buffer
    event_buffer = []
    fifo_event_buffer = []

    # Timing machine
    current_task = AvailableCurrentTasks.IDLE
    tic = time.time()
    passed = -1
    frame_count = 0

    def __init__(self):
        super().__init__()
        self.win.winHandle.activate()
        self.set_as_idle_screen()
        logger.info('Initialized')

    def set_as_idle_screen(self):
        self.osd_timer_slogan.autoDraw = True
        self.osd_user_profile.autoDraw = True
        self.osd_prompt_slogan.autoDraw = True
        self.blinking_pnt.autoDraw = True
        logger.debug('Set as debug mode')

    def ssvep__stop__(self):
        self.img_full_screen.setAutoDraw(False)
        del self.img_full_screen
        self.img_full_screen = None
        del self.total_length

        self.set_as_idle_screen()

        self.tic = time.time()
        self.frame_count = 0
        self.osd_prompt_slogan_text = 'SSVEP experiment finished'

        logger.debug(f'SSVEP experiment finished, {self.event_buffer}')
        self.fifo_event_buffer.append(list(self.event_buffer))

    def ssvep__init__(
            self, resolution_x=None, resolution_y=None,
            repeats=None, cue=None,
            df_layout=None, df_ts=None,
            head_length=None, body_length=None, tail_length=None,
            background_image_data_url=None,
            patch_shape=None,
            ** kwargs):

        if background_image_data_url == '' or background_image_data_url is None:
            logger.debug('background image is empty')
            img = Image.fromarray(
                np.zeros((resolution_y, resolution_x))).convert('RGB')
        else:
            logger.debug('background image is provided')
            img = convert_data_url_to_img(background_image_data_url).convert('RGB').resize(
                (resolution_x, resolution_y))

        draw = ImageDraw.Draw(img)
        self.img = img
        self.draw = draw
        print(img)

        img_full_screen = visual.ImageStim(win=self.win, image=img)
        self.img_full_screen = img_full_screen

        # Put the timer on the top center
        self.osd_timer_slogan.pos = (0, resolution_y/2 - 20)
        # Put the pnt on the north-east corner
        self.blinking_pnt.pos = (resolution_x/2-10, resolution_y/2-10)

        # --------------------
        self.patch_shape = patch_shape
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
        self.total_length = self.trial_length * self.repeats
        self.last_state = 'init'

        self.ssvep_mk_patches()

        self.osd_user_profile.setAutoDraw(False)
        self.osd_prompt_slogan.setAutoDraw(False)
        for e in [self.img_full_screen, self.osd_timer_slogan, self.blinking_pnt]:
            e.setAutoDraw(False)
            e.setAutoDraw(True)

        self.event_buffer = []

        logger.debug('Initialized SSVEP')

    def ssvep_mk_patches(self):
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

    def ssvep_update_frame(self, passed):
        t = passed % (self.trial_length)
        i = np.min([self.repeats-1, int(passed // self.trial_length)])

        state = 'head'
        if t > self.head_length:
            state = 'body'
        if t > self.head_length + self.body_length:
            state = 'tail'

        self.osd_timer_slogan.text += f' | {i+1} trial | {state}'

        if state == 'head':
            cue = self.trials_cue[i]
            for k, se in self.patches.items():
                xy = se['xy']

                if se['name'] == cue:
                    if self.patch_shape == 'rectangle':
                        self.draw.rectangle(xy=xy, fill=gray2rgb(255))
                    elif self.patch_shape == 'ellipse':
                        self.draw.ellipse(xy=xy, fill=gray2rgb(255))
                else:
                    if self.patch_shape == 'rectangle':
                        self.draw.rectangle(xy=xy, fill=gray2rgb(100))
                    elif self.patch_shape == 'ellipse':
                        self.draw.ellipse(xy=xy, fill=gray2rgb(100))

            self.img_full_screen.image = self.img

            if not self.last_state == 'head':
                self.event_buffer.append(('displayHead', cue, passed))

        if state == 'body':
            tt = t - self.head_length
            j = len(self.seconds[self.seconds < tt])
            for k, se in self.patches.items():
                try:
                    xy = se['xy']
                    x = self.ts_objs[k][j]

                    if self.patch_shape == 'rectangle':
                        self.draw.rectangle(xy=xy, fill=gray2rgb(int(x*255)))
                    elif self.patch_shape == 'ellipse':
                        self.draw.ellipse(xy=xy, fill=gray2rgb(int(x*255)))

                except Exception:
                    pass
            self.img_full_screen.image = self.img

            if not self.last_state == 'body':
                self.event_buffer.append(('displayBody', passed))

        if state == 'tail':
            for k, se in self.patches.items():
                xy = se['xy']

                if self.patch_shape == 'rectangle':
                    self.draw.rectangle(xy=xy, fill=gray2rgb(100))
                elif self.patch_shape == 'ellipse':
                    self.draw.ellipse(xy=xy, fill=gray2rgb(100))

            self.img_full_screen.image = self.img

            if not self.last_state == 'tail':
                self.event_buffer.append(('displayTail', passed))

        self.last_state = state

        self._update_pnt_color()
        self.win.flip()
        return passed

    def main_loop(self):
        logger.debug('Starting main loop...')
        while True:
            if self.current_task == AvailableCurrentTasks.IDLE:
                self._on_frame_flip()
                self.osd_prompt_slogan.text = self.osd_prompt_slogan_text
                # self.osd_prompt_slogan.draw()
                self.osd_user_profile.text = self.osd_user_profile_text

                if len(self.task_buffer) == 0:
                    self.win.flip()
                    continue

                name, stuff = self.task_buffer.pop(0)

                logger.debug(f'Received task: {name}, stuff: {list(stuff)}')

                if name == 'SSVEP':
                    try:
                        self.ssvep__init__(**stuff)
                        self.ssvep_mk_patches()
                        self.start_task(AvailableCurrentTasks.SSVEP)
                    except Exception as error:
                        logger.error(f'Failed to initialize SSVEP: {error}')
                        import traceback
                        traceback.print_exc()

                    self.win.flip()
                    continue

            if self.current_task == AvailableCurrentTasks.SSVEP:
                passed = self._on_frame_flip()
                if passed > self.total_length:
                    self.ssvep__stop__()
                    self.current_task = AvailableCurrentTasks.IDLE
                    logger.debug('SSVEP finished')
                    continue

                self.ssvep_update_frame(passed)
                self.win.flip()
                continue

        logger.debug(f'Finished main loop...')
        self.safe_stop()

    def start_task(self, task):
        self.tic = time.time()
        self.frame_count = 0
        self.current_task = task

    def safe_stop(self):
        self.win.close()
        core.quit()
        logger.debug('Stopped psychopy window')

    def _on_frame_flip(self):
        self._update_pnt_color()
        passed = self._update_timer()
        if key_pressed := kb.getKeys():
            name = key_pressed[0].name
            self.event_buffer.append(('keyPress', name, passed))
            logger.debug(f'Key pressed", {key_pressed}')
        return passed

    def _update_timer(self):
        passed = time.time() - self.tic
        self.passed = passed
        self.frame_count += 1

        minutes = int(passed // 60)
        seconds = int((passed // 1) % 60)
        remain = int((passed % 1)*100)

        frame_rate = self.frame_count / np.max([passed, 0.1])

        self.osd_timer_slogan.text = f'{minutes}:{seconds:02d}:{remain:02d} | {frame_rate:0.2f}Hz'
        return passed

    def _update_pnt_color(self):
        self.blinking_pnt.color = random_color()


# %% ---- 2024-06-05 ------------------------
# Play ground


# %% ---- 2024-06-05 ------------------------
# Pending


# %% ---- 2024-06-05 ------------------------
# Pending
