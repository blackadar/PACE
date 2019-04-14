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
    :return: X and y for a SciKitLearn model
    """
    train = pd.concat([pd.Series(strip_date(telemetry.index)[:, 0]), telemetry['Congestion'].reset_index()], axis=1)
    train = train.drop('Interval', axis='columns').set_index(0).sort_index()
    return np.array(train.index).reshape(-1, 1), train['Congestion']


def model_svr(times, congestion, C_=.5, gamma_=.0001):
    """
    Models Area congestion based on time and congestion data
    :param preprocessed_data: Data run through pre-processing
    :return:
    """
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(times, congestion, random_state=42, train_size=0.7)
    model = SVR(kernel='rbf', C=C_, gamma=gamma_)
    model.fit(X_train, y_train)
    print("Train accuracy is %.2f %%" % (model.score(X_train, y_train) * 100))
    print("Test accuracy is %.2f %%" % (model.score(X_test, y_test) * 100))
    return model


def model_ridge(times, congestion):
    """
    Models Area congestion based on time and congestion data
    :param preprocessed_data: Data run through pre-processing
    :return:
    """
    from sklearn import linear_model
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(times, congestion, random_state=42, train_size=0.7)
    model = linear_model.Ridge(alpha=.5)
    model.fit(X_train, y_train)
    print("Train accuracy is %.2f %%" % (model.score(X_train, y_train) * 100))
    print("Test accuracy is %.2f %%" % (model.score(X_test, y_test) * 100))
    return model


def model_poly_ridge(times, congestion):
    import matplotlib.pyplot as plt

    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import make_pipeline
    from sklearn.model_selection import train_test_split

    plt.scatter(times[:, 0], congestion.to_numpy, color='navy', s=30, marker='o', label="training points")

    for count, degree in enumerate([3, 4, 5, 6, 7]):
        model = make_pipeline(PolynomialFeatures(degree), Ridge())
        model.fit(times, congestion)
        y_plot = model.predict(times)
        plt.plot(times.index, y_plot, linewidth=2,
                 label="degree %d" % degree)
    plt.legend()
    plt.show()

    X_train, X_test, y_train, y_test = train_test_split(times, congestion, random_state=42, train_size=0.5)

    model = make_pipeline(PolynomialFeatures(6), Ridge())
    model.fit(X_train, y_train)
    print("Train accuracy is %.2f %%" % (model.score(X_train, y_train) * 100))
    print("Test accuracy is %.2f %%" % (model.score(X_test, y_test) * 100))
    return model


def main():
    """
    Testing! Really just a place to save what I've been doing in console.
    :return:
    """
    import pace.analysis.read as rd
    import pace.analysis.learn as lrn
    import pace.analysis.plot as pplt
    telemetry = rd.pickle_jar(rd.find_all_pickles('data/'))
    train = lrn.preprocess(telemetry)
    k = lrn.model_svr(*train)
    pplt.eval_model(*train, k).show()
