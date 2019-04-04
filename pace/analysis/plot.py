"""
Look at this graph
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn

seaborn.set()


def congestion(telemetry: pd.DataFrame):
    """
    Plot congestion over time
    :param telemetry: Processed Simple DataFrame
    :return: matplotlib.figure
    """
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.set_title("Area Congestion")
    ax.set_xlabel("Time")
    ax.set_ylabel("Congestion")
    im = ax.plot(telemetry['Number Devices'] / telemetry['Number Devices'].max())
    return figure


def polyfit_congestion(telemetry: pd.DataFrame, poly_degree=8):
    """
    Plot polynomial fit congestion over time
    :param poly_degree: Degree of polynomial fit
    :param telemetry: Processed Simple DataFrame
    :return: matplotlib.figure
    """
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.set_title("Area Congestion")
    ax.set_xlabel("Time")
    ax.set_ylabel("Congestion")

    conv_times = mdates.date2num(telemetry.index.to_list())

    y_values = telemetry['Number Devices'] / telemetry['Number Devices'].max()
    x_values = np.linspace(0, 1, len(telemetry.loc[:, "Number Devices"]))

    coeffs = np.polyfit(x_values, y_values, poly_degree)
    poly_eqn = np.poly1d(coeffs)
    y_hat = poly_eqn(x_values)

    im = ax.plot(telemetry.index, y_hat)
    return figure
