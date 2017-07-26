import statsmodels.formula.api as smf
import pandas as pd


class MultiLinearRegression:

    def __init__(self, data):
        self.data = data
        self.format_data()
        self.train = data[:-30]
        self.test = data[-30:]
        self.results_formula = None

    # Because the data have an seasonal pattern we need to create variables that
    # can represent the season pattern first create the columns
    def format_data(self):
        self.data['d1'] = 0
        self.data['d2'] = 0
        self.data['d3'] = 0
        self.data['d4'] = 0
        self.data['d5'] = 0
        self.data['d6'] = 0

        # fill the columns with the correct dat. a 1 if it is the day of the week.
        for i in range(len(self.data)):
            weekday = self.data.weekday[i]
            if weekday != 7:
                self.data.set_value(i, "d%d" % weekday, 1)

        # Set the date as index
        self.data.index = pd.to_datetime(self.data.date, format="%d/%m/%Y")

    def fit_model(self):
        """ After we prepare the data we must train the model.
        First we write down the formula than fit the data.
        at the end we return the coefficients of the model so we can show them to the user"""
        model = smf.ols(formula='sales ~ holiday + d1+d2+d3+d4+d5+d6+ temp+ weather', data=self.train)

        self.results_formula = model.fit()
        coefficient = self.results_formula.params
        df = coefficient.tolist()
        return df

    def predict(self):
        results = self.results_formula.predict(self.test)
        return results
