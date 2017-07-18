import warnings
import itertools
import pandas as pd
import numpy as np
from datetime import datetime
import statsmodels.api as sm
import matplotlib.pyplot as plt

class Arima:

    def __init__(self,data):
        self.data = data[:-30]
        self.data['index'] = pd.to_datetime(self.data['date'])
        self.data.set_index(['index'], inplace=True)
        self.data.index.name = None

        self.test = data[-30:]
        self.test['index'] =data[-30:]['date']
        self.test.set_index(['index'], inplace=True)
        self.test.index.name = None

        self.model = None

    def grid_search(self, season_length):

        print(sm.version)

        # Define the p, d and q parameters to take any value between 0 and 2
        p = d = q = range(0, 3)

        # Generate all different combinations of p, q and q triplets
        pdq = list(itertools.product(p, d, q))

        # Generate all different combinations of seasonal p, q and q triplets
        seasonal_pdq = [(x[0], x[1], x[2], season_length) for x in list(itertools.product(p, d, q))]

        warnings.filterwarnings("ignore") # specify to ignore warning messages

        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(self.data.sales,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)

                    results = mod.fit(disp=0)

                    print('ARIMA{}x{}7 - AIC:{}'.format(param, param_seasonal, results.aic))
                except:
                    continue

    def fit_model(self,season_length):
        warnings.filterwarnings("ignore") # specify to ignore warning messages
        mod = sm.tsa.statespace.SARIMAX(self.data.sales,
                                        order=(1, 1, 2),
                                        seasonal_order=(1, 2, 2, season_length),
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)

        self.model = mod.fit(disp=0)

    def predict(self, nr):
        pred = self.model.forecast(nr)
        return pred
