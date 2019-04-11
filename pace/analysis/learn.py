"""
We've learned a lot.
Can the computer?
"""
import numpy as np
import pandas as pd
from sklearn.svm import SVR


def strip_date(datetimes: pd.Series):
    """
    Converts a series of DateTimes to time only.
    :param datetimes: DateTime Series
    :return: Time Only Series
    """
    return np.array([x.hour * 60 + x.minute for x in datetimes])[:, np.newaxis]


def model(times, congestions):
    """
    Models Area congestion based on time and congestion data
    :param times: Time Only series
    :param congestions: Associated congestion values
    :return:
    """
    svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
    y_rbf = svr_rbf.fit(times[:, 1], congestions).predict(times[:, 1])
