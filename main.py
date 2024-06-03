"""
File: main.py
Author: Chuncheng Zhang
Date: 2024-06-03
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Main entrance for the program

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-06-03 ------------------------
# Requirements and constants
from flask import Flask, render_template
from pathlib import Path

from util import logger

root = Path(__file__).parent
web = root.joinpath('web')

app = Flask(
    'libowen-ssvep-program',
    static_url_path='/static',
    static_folder=web.joinpath('static'),
    template_folder=web.joinpath('template')
)

# %% ---- 2024-06-03 ------------------------
# Function and class


@app.route("/", methods=["GET", "POST"])
def root():
    return render_template('index.html')


# %% ---- 2024-06-03 ------------------------
# Play ground
if __name__ == "__main__":
    app.run(port=23333, debug=True)


# %% ---- 2024-06-03 ------------------------
# Pending


# %% ---- 2024-06-03 ------------------------
# Pending
