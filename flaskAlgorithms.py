from flask import Flask
from flask import render_template
from flask import Response
import json
from Algorithms.HoltWinters import HoltWinters
import pandas as pd
import numpy as np
import os
from settings import APP_STATIC
import csv

app = Flask(__name__)


@app.route('/holt-winters', methods = ['GET'])
def holt_winters():
    data = get_date()
    hw = HoltWinters(data["sales"])

    result = hw.triple_exponential_smoothing(7, 0.8, 0.3, 0.9, 30)[-30:]
    best_error = validater(result, hw.test)

    data_response = {'error' : best_error}
    js = json.dumps(data_response)

    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/')
def hello_world():
    data = get_date()
    hw = HoltWinters(data["sales"])

    result = hw.triple_exponential_smoothing(7, 0.8, 0.3, 0.9, 30)[-30:]
    best_error = validater(result, hw.test)
    return render_template('index.html', error=0)

def validater(result, test):
    # The mean squared error
    return np.mean((result - test) ** 2)


def get_date():
    data = pd.read_csv(os.path.join(APP_STATIC, 'data.csv'))
    data["date"] = pd.to_datetime(data["date"])
    return data


if __name__ == '__main__':
    app.run()
