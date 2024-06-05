"""
File: try-psychopy.py
Author: Chuncheng Zhang
Date: 2024-06-05
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


# %% ---- 2024-06-05 ------------------------
# Requirements and constants
from util.display import MainWindow, core


# %% ---- 2024-06-05 ------------------------
# Function and class


# %% ---- 2024-06-05 ------------------------
# Play ground
if __name__ == "__main__":
    main_window = MainWindow()
    while True:
        if main_window.update_frame() > 30:
            break

    main_window.win.close()
    core.quit()

# %% ---- 2024-06-05 ------------------------
# Pending


# %% ---- 2024-06-05 ------------------------
# Pending
