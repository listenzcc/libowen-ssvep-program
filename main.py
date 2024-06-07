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
import pickle
import plotly.express as px

from pathlib import Path

from flask import Flask, Response, render_template, request

from util import logger
from util.websocket_client import MyWebsocketClient
from util.session_manager import SessionManager, TimeSeriesManager, txt2df


# ----------------------------------------
# ---- Initialize objects ----

root = Path(__file__).parent
web = root.joinpath('web')

sm = SessionManager(root.joinpath('asset/design'))
tsm = TimeSeriesManager(root.joinpath('asset/timeseries'))

app = Flask(
    'libowen-ssvep-program',
    static_url_path='/static',
    static_folder=web.joinpath('static'),
    template_folder=web.joinpath('template')
)

mwc = MyWebsocketClient()

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


@app.route('/getByName', methods=['GET'])
def get_by_name():
    name = request.args.get('name')
    sm.refresh()
    content = sm.get_by_name(name)
    logger.debug(f'Got by name: {name}')
    return dict(content=content)


@app.route('/getTimeSeries', methods=['GET'])
def get_time_series():
    name = request.args.get('name')
    df = tsm.get_by_name(name)
    logger.debug(f'Got by name: {name}')
    return df.to_json()


@app.route('/commitTemporal', methods=['POST'])
def commit_temporal():
    body_length = request.form.get('trialBodyLength')
    txt = request.form.get('designText')
    df_ts, df_corr = tsm.merge_with_txt(txt, body_length)

    fig1 = px.line(
        df_ts,
        x='seconds',
        y='value',
        facet_row='type',
        symbol='type',
        symbol_map={'ts': 'line-ew', 'compute': 'line-ns'},
        color='name',
        template="seaborn")

    fig2 = px.imshow(df_corr, template="seaborn")

    return render_template(
        "time-series.html",
        fig1=fig1.to_html(full_html=False),
        fig2=fig2.to_html(full_html=False))


@app.route('/go', methods=['POST'])
def _go():
    head_length = request.form.get('trialHeadLength')
    body_length = request.form.get("trialBodyLength")
    tail_length = request.form.get("trialTailLength")
    txt = request.form.get('designText')
    cue = request.form.get('cue')
    repeats = request.form.get("trialRepeats")
    resolution_x = request.form.get("resolutionX")
    resolution_y = request.form.get("resolutionY")

    df_ts, _ = tsm.merge_with_txt(txt, body_length)
    df_layout = txt2df(txt)

    print(df_layout)
    print(df_ts)
    print(cue, head_length, body_length, tail_length, repeats)
    print(resolution_x, resolution_y)

    kwargs = dict(
        task_name='SSVEP',
        prompt='SSVEP Experiment Prompt',
        resolution_x=int(resolution_x),
        resolution_y=int(resolution_y),
        repeats=int(repeats),
        cue=cue,
        df_layout=df_layout,
        df_ts=df_ts,
        head_length=int(head_length),
        body_length=int(body_length),
        tail_length=int(tail_length),
    )
    print(kwargs)

    try:
        mwc.send(pickle.dumps(dict(prompt='Hello')))
        mwc.send(pickle.dumps(kwargs))
    except Exception as error:
        import traceback
        logger.error(f'Failed websocket connection: {error}')
        return dict(suggestion='Open the display', error=f'{error}', traceback=traceback.format_exc()), 500

    return dict(go='go')


@app.route('/setUserProfile', methods=['POST'])
def userLogin():
    pkg = dict(request.form.items())

    try:
        mwc.send(pickle.dumps(dict(
            task_name='setUserProfile',
            profile=pkg
        )))
    except Exception as error:
        import traceback
        logger.error(f'Failed websocket connection: {error}')
        return dict(suggestion='Open the display', error=f'{error}', traceback=traceback.format_exc()), 500

    return dict(msg='UserLogin')


@app.route('/checkoutDisplayStatus', methods=['GET'])
def checkout_display_status():
    try:
        got = mwc.send(pickle.dumps(dict(
            task_name='checkoutDisplayStatus',
        )))
        msg = pickle.loads(got)
        print(msg)
        return msg
    except Exception as error:
        import traceback
        logger.error(f'Failed websocket connection: {error}')
        return dict(suggestion='Open the display', error=f'{error}', traceback=traceback.format_exc()), 500


# %% ---- 2024-06-03 ------------------------
# Play ground
if __name__ == "__main__":
    app.run(port=23333, debug=True)


# %% ---- 2024-06-03 ------------------------
# Pending


# %% ---- 2024-06-03 ------------------------
# Pending
