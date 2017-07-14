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


@app.route('/holt-winters-params', methods = ['GET'])
def holt_winters_params():
    data = get_date()
    hw = HoltWinters(data["sales"])
    result = hw.triple_exponential_smoothing(7, 0.0, 0.0, 0.0, 30)[-30:]
    best_error = validater(result, hw.test)
    best_result = [0.1, 0.1, 0.1, best_error]
    all_better_results = [[0.0, 0.0, 0.0, best_error]]

    # Try all parameters and check what is the best combination
    prop = [round(x * 0.1, 1) for x in range(0, 10)]
    for alpha in prop:
        for beta in prop:
            for gamma in prop:
                result = hw.triple_exponential_smoothing(7, alpha, beta, gamma, 30)[-30:]

                # check if current params gives a better result if so store them
                if validater(result, hw.test) < best_error:
                    best_error = validater(result, hw.test)
                    best_result = [alpha, beta, gamma, best_error]
                    all_better_results.append(best_result)

    data_response = {
        'best': best_result,
        'all_better_results': all_better_results
    }

    js = json.dumps(data_response)

    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/holt-winters', methods = ['GET'])
def holt_winters():
    data = get_date()
    hw = HoltWinters(data["sales"])

    result = hw.triple_exponential_smoothing(7, 0.8, 0.5, 0.1, 30)[-30:]
    mse = validater(result, hw.test)
    average_error = average(result, hw.test)
    mae = mean_absolute_error(result, hw.test)
    mape = mean_absolute_percentage_error(result, hw.test)

    data_response = {
        'mse': mse,
        'average': average_error,
        'mae': mae,
        'mape': mape

    }

    js = json.dumps(data_response)

    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/')
def hello_world():
    return render_template('index.html', error=0)


def validater(result, test):
    """" returns the mean squared error"""
    return float("{0:.4f}".format(np.mean((result - test) ** 2)))


def average(result, test):
    """" returns the average"""
    sum_e = 0
    for i in range(0,len(result)-1):
        sum_e += result[i] - test[i]

    return float("{0:.4f}".format(sum_e / float(len(result))))


def mean_absolute_error(result, test):
    """ returns the mean absolute error """
    sum_e = 0
    for i in range(0, len(result) - 1):
        sum_e += np.absolute((result[i] - test[i]))

    return float("{0:.4f}".format(sum_e / float(len(result))))


def mean_absolute_percentage_error(result, test):
    """ returns the mean absolute percentage error """
    sum_e = 0
    for i in range(0, len(result) - 1):
        sum_e += np.absolute(((result[i] - test[i]) / test[i]))

    return float("{0:.4f}".format(100*(sum_e / float(len(result)))))


def get_date():
    data = pd.read_csv(os.path.join(APP_STATIC, 'data.csv'))
    data["date"] = pd.to_datetime(data["date"])
    return data


if __name__ == '__main__':
    app.run()
