
class HoltWinters:

    def __init__(self,data):
        self.train = data[:-30].values
        self.test = data[-30:].values

    # Moving average using n last points
    def average(self, n=None):

        if n is None:
            return self.average(self.train, len(self.train))
        return float(sum(self.train[-n:])) / n

    # Weighted average, weights is a list of weights
    def weighted_average(self, weights):

        result = 0.0
        weights.reverse()

        for n in range(len(weights)):
            result += self.train[-n - 1] * weights[n]
        return result

    # Given a series and alpha, return series of smoothed points
    def exponential_smoothing(self, alpha, number_predictions):

        # first value is same as series
        result = [self.train[0]]

        for n in range(1, len(self.train) + number_predictions):

            if n >= len(self.train):
                value = result[-1]
                data_point = self.train[len(self.train) - 1]
            else:
                value = result[n - 1]
                data_point = self.train[n]

            result.append(alpha * data_point + (1 - alpha) * value)

        return result

    # Given a series ,alpha ans beta, return series of smoothed points
    def double_exponential_smoothing(self, alpha, beta, number_predictions):
        result = [self.train[0]]

        for n in range(1, len(self.train) + number_predictions):

            if n == 1:
                level, trend = self.train[0], self.train[1] - self.train[0]

            # we are forecasting
            if n >= len(self.train):
                value = result[len(self.train) - 1]

            else:
                value = self.train[n]

            last_level, level = level, alpha * value + (1 - alpha) * (level + trend)
            trend = beta * (level - last_level) + (1 - beta) * trend
            result.append(level + trend)

        return result

    # Get the trend in in the data
    def initial_trend(self, season_length):
        sum = 0.0
        for i in range(season_length):
            sum += float(self.train[i + season_length] - self.train[i]) / season_length
        return sum / season_length

    # Get the seasonal components
    def initial_seasonal_components(self, season_length):
        seasonals = {}
        season_averages = []
        n_seasons = int(len(self.train) / season_length)

        # compute season averages
        for j in range(n_seasons):
            season_averages.append(
                sum(self.train[season_length * j:season_length * j + season_length]) / float(season_length)
            )

        # compute initial values
        for i in range(season_length):
            sum_of_vals_over_avg = 0.0
            for j in range(n_seasons):
                sum_of_vals_over_avg += self.train[season_length * j + i] - season_averages[j]
            seasonals[i] = sum_of_vals_over_avg / n_seasons

        return seasonals

    # Given a series, alpha, beta , gamma and the number of predictions. return series of smoothed points
    def triple_exponential_smoothing(self, slen, alpha, beta, gamma, n_preds):
        result = []
        seasonals = self.initial_seasonal_components(slen)

        for i in range(len(self.train) + n_preds):

            # initial values
            if i == 0:
                smooth = self.train[0]
                trend = self.initial_trend(slen)
                result.append(self.train[0])
                continue

            # we are forecasting
            if i >= len(self.train):
                m = i - len(self.train) + 1
                result.append((smooth + m * trend) + seasonals[i % slen])

            else:
                val = self.train[i]
                last_smooth, smooth = smooth, alpha * (val - seasonals[i % slen]) + (1 - alpha) * (smooth + trend)
                trend = beta * (smooth - last_smooth) + (1 - beta) * trend
                seasonals[i % slen] = gamma * (val - smooth) + (1 - gamma) * seasonals[i % slen]
                result.append(smooth + trend + seasonals[i % slen])

        return result

