from flask import Flask
from flask import render_template
from flask import Response
import json
from Algorithms.HoltWinters import HoltWinters
from Algorithms.MultiLinearRegression import MultiLinearRegression
from Algorithms.ARIMA import Arima
import pandas as pd
import numpy as np
import os
from settings import APP_STATIC

app = Flask(__name__)


@app.route('/holt-winters-params', methods = ['GET'])
def holt_winters_params():
    # Get the data en initialize the Holt-Winters class
    data = get_date()
    hw = HoltWinters(data["sales"])

    # Initialize parameters for tracking the best parameters
    result = hw.triple_exponential_smoothing(7, 0.0, 0.0, 0.0, 30)[-30:]
    best_error = mean_squared_error(result, hw.test)
    best_result = [0.0, 0.0, 0.0, best_error]
    all_better_results = [[0.0, 0.0, 0.0, best_error]]

    # Try all parameters and check what is the best combination
    prop = [round(x * 0.1, 1) for x in range(0, 10)]
    for alpha in prop:
        for beta in prop:
            for gamma in prop:
                result = hw.triple_exponential_smoothing(7, alpha, beta, gamma, 30)[-30:]

                # Check if current params gives a better result if so store them
                if mean_squared_error(result, hw.test) < best_error:
                    best_error = mean_squared_error(result, hw.test)
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
    # Get the data en initialize the Holt-Winters class
    data = get_date()
    hw = HoltWinters(data["sales"])

    # Get the error measures of the model
    result = hw.triple_exponential_smoothing(7, 0.8, 0.5, 0.1, 30)[-30:]
    mse = mean_squared_error(result, hw.test)
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


@app.route('/multi', methods=['GET'])
def multi_linear_regression():
    # Get the data en initialize the MultiLinearRegression class
    data = get_date()
    mlr = MultiLinearRegression(data)

    # Fit the model and make predictions
    coef = mlr.fit_model()
    result = mlr.predict()

    # Get the error measures of the model
    mse = mean_squared_error(result, data["sales"][-30:])
    average_error = average(result, data["sales"][-30:])
    mae = mean_absolute_error(result, data["sales"][-30:])
    mape = mean_absolute_percentage_error(result, data["sales"][-30:])

    data_response = {
        'coef' :coef,
        'mse': mse,
        'average': average_error,
        'mae': mae,
        'mape': mape

    }

    js = json.dumps(data_response)

    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/arima', methods=['GET'])
def arima():
    # Get the data en initialize the Arima class
    data = get_date()
    ar = Arima(data)

    # Fit the model and make a prediction. Uncomment grid
    # ar.grid_search(7)
    ar.fit_model(7)
    result = ar.predict(30)

    # Get the error measures of the model
    mse = mean_squared_error(result.values, data["sales"][-30:].values)
    average_error = average(result.values, data["sales"][-30:].values)
    mae = mean_absolute_error(result.values, data["sales"][-30:].values)
    mape = mean_absolute_percentage_error(result.values, data["sales"][-30:].values)

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
def home():
    return render_template('index.html', error=0)


def mean_squared_error(result, test):
    """ returns the mean squared error """
    return float("{0:.4f}".format(np.mean((result - test) ** 2)))


def average(result, test):
    """ returns the average"""
    sum_e = 0
    for i in range(0,len(result)-1):
        sum_e += result[i] - test[i]

    return float("{0:.4f}".format(sum_e / float(len(result))))


def mean_absolute_error(result, test):
    """ Returns the mean absolute error """
    sum_e = 0
    for i in range(0, len(result) - 1):
        sum_e += np.absolute((result[i] - test[i]))

    return float("{0:.4f}".format(sum_e / float(len(result))))


def mean_absolute_percentage_error(result, test):
    """ Returns the mean absolute percentage error """
    sum_e = 0
    for i in range(0, len(result) - 1):
        sum_e += np.absolute(((result[i] - test[i]) / test[i]))

    return float("{0:.4f}".format(100*(sum_e / float(len(result)))))


def get_date():
    """ Import the data as dataframe and make the date column a date object """
    data = pd.read_csv(os.path.join(APP_STATIC, 'data.csv'))
    data["date"] = pd.to_datetime(data["date"],format="%d/%m/%Y")
    return data


if __name__ == '__main__':
    app.run()
