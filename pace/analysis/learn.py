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


def preprocess(telemetry: pd.DataFrame):
    """
    Mold the data into ML training data
    :param telemetry: Area telemetry data
    :return: DataFrame of index:absolute day min, Congestion: congestion val
    """
    train = pd.concat([pd.Series(strip_date(telemetry.index)[:, 0]), telemetry['Congestion'].reset_index()], axis=1)
    train = train.drop('Interval', axis='columns').set_index(0)
    return train


def model(preprocessed_data):
    """
    Models Area congestion based on time and congestion data
    :param preprocessed_data: Data run through pre-processing
    :return:
    """
    svr_rbf = SVR(kernel='rbf', C=1, gamma=0.1, epsilon=.01)
    times = np.array(preprocessed_data.index)
    congestion = preprocessed_data['Congestion']
    y_rbf = svr_rbf.fit(times.reshape(-1, 1), congestion)  # .predict(times[:, 1])
    return y_rbf


def main():
    """
    Testing! Really just a place to save what I've been doing in console.
    :return:
    """
    import pace.analysis.read as rd
    import pace.analysis.learn as lrn
    import matplotlib.pyplot as plt
    import numpy as np
    telemetry = rd.pickle_jar(rd.find_all_pickles('data/'))
    train = lrn.preprocess(telemetry)
    plt.scatter(train.index, train['Congestion'])
    plt.show()
    k = lrn.model(train)
    prediction = k.predict(np.arange(1440).reshape(-1, 1))
    plt.scatter(np.arange(1440), prediction)
    plt.show()
    plt.plot(np.arange(1440), prediction)
    plt.show()
    score = k.score(np.array(train.index).reshape(-1, 1), train['Congestion'])
    print('Score: ', score)
