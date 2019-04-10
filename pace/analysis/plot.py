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
    figure = plt.figure(figsize=(20, 4))
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


def devices_per_probes(telemetry: pd.DataFrame):
    """
    plot number of devices per number of probes
    :param telemetry: Processed Simple DataFrame
    :return: mathplotlib.figure
    """
    figure = plt.figure(figsize=(20, 4))
    ax = figure.add_subplot(111)
    ax.set_title("Devices Per Request")
    ax.set_xlabel("Number of Devices")
    ax.set_ylabel("Number of Requests")
    mi = ax.plot(telemetry['Devices'] / telemetry['Total Probes'])
    return figure


def devices_per_interval(telemetry: pd.DataFrame):
    """
    plot number of devices per each interval
    :param telemetry: Processed Simple Dataframe
    :return: mathplotlib.figure
    """
    figure = plt.figure(figsize=(20, 4))
    ax = figure.add_subplot(111)
    ax.set_title("Devices per Interval")
    ax.set_xlabel("Time")
    ax.set_ylabel("Number of Devices")
    mi = ax.plot(telemetry['Number Devices'] / telemetry['Interval'])
    return figure


def probes_per_time_vs_devices_per_interval(telemetry: pd.DataFrame):
    """
    plot number of probes per time versus number of devices per time interval
    :param telemetry: Processed Simple DataFrame
    :return: mathplotlib.figure
    """
    figure = plt.figure(figsize=(20, 4))
    ax = figure.add_subplot(111)
    ax.set_title("Requests per Time over Devices per Interval")
    ax.set_xlabel("Devices per Interval")
    ax.set_ylabel("Requests per Time")
    probes_per_time = telemetry['Total Probes'] / telemetry['Interval']
    requests_per_interval = telemetry['Number SSID Requests']/telemetry['Interval']
    mi = ax.plot(probes_per_time/requests_per_interval)
    return figure


def SSID_freq(telemetry: pd.DataFrame):
    """
    plot frequency of the request of each SSID
    :param telemetry: Processed Simple DataFrame
    :return: mathplotlib.figure
    """
    figure = plt.figure(figsize=(20, 4))
    ax = figure.add_subplot(111)
    ax.set_title("SSID Frequency")
    ax.set_xlabel("SSID")
    ax.set_ylabel("number of requests")
    mi = ax.plot(telemetry['SSID Requests']/telemetry['Number SSID Requests'])
    return figure
