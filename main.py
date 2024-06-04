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
import json
from flask import Flask, render_template, request
from pathlib import Path

from util import logger
from util.session_manager import SessionManager

root = Path(__file__).parent
web = root.joinpath('web')

sm = SessionManager(root.joinpath('asset/design'))

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


@app.route('/commit', methods=["POST"])
def commit():
    name = request.form.get("designName")
    txt = request.form.get('designText')
    sm.save(name, txt)
    dfs = sm.refresh()
    logger.debug(f'Received new design {name}')
    return list(dfs.keys())


@app.route('/getAll', methods=['GET'])
def get_all():
    names = list(sm.refresh().keys())
    logger.debug(f'Got names: {names}')
    return names


@app.route('/get', methods=['GET'])
def get_by_name():
    name = request.args.get('name')
    print(name)
    sm.refresh()
    return dict(content=sm.get_by_name(name))


# %% ---- 2024-06-03 ------------------------
# Play ground
if __name__ == "__main__":
    app.run(port=23333, debug=True)


# %% ---- 2024-06-03 ------------------------
# Pending


# %% ---- 2024-06-03 ------------------------
# Pending
