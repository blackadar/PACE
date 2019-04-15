"""
Handles data input to analysis
"""
import codecs
import json
import logging
import os
import urllib.request as urllib2

import numpy as np
import pandas as pd


def check_create_data():
    """
    Check for the data/ directory.
    Create it if it does not exist.
    :return:
    """
    logging.debug("Checking data path...")
    dirs = os.listdir(os.getcwd())
    if 'data' not in dirs:
        logging.info("Data Directory not found, creating it...")
        os.mkdir('data')


def data_exists(path):
    """
    Check if the data directory has files
    :return: Boolean Has Files
    """
    return len(os.listdir(path)) != 0


def clear_data(path):
    """
    Empty the data directories
    :return: None
    """
    import os
    logging.info("Removing existing data in " + str(path))
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print("[!] " + str(e))


def delete_file(path):
    """
    Deletes the path file
    :param path:
    :return:
    """
    logging.info("Removing existing file at " + str(path))
    os.remove(path)


def open_pickle(path):
    """
    Un-pickles a file at path.
    WARNING: NEVER UN-PICKLE AN UNKNOWN FILE!
    Python is 100% trusting of a pickle.
    Hacked pickles can ruin a burger.
    :param path: Path (relative or absolute) to pickle
    :return: Un-pickled thing
    """
    import pickle
    with open(path, "rb") as pkl:
        return pickle.load(pkl)


def find_all_pickles(path: str):
    """
    Finds and un-pickles all pickles in a directory
    :param path: Path to pickles
    :return: List of Pickles
    """
    ret = []
    for file in os.listdir(path):
        if file.endswith(".pkl"):
            ret.append(open_pickle(os.path.join(path, file)))
    return ret


def pickle_to_series(pickle_data: dict):
    """
    Translate Pickle Data into a Series with Simple Sizes
    :param pickle_data: Dictionary from pace.analysis.read.un_pickle
    :return: Pandas Series
    """
    simple = {
        'Interval': pickle_data['Interval'],  # start of interval
        'Devices': pickle_data['Devices'],  # set of mac addresses
        'Number Devices': len(pickle_data['Devices']),  # size of set of mac addresses
        'SSID Requests': pickle_data['SSID Requests'],  # which network devices are looking for
        'Number SSID Requests': len(pickle_data['SSID Requests']),  # length of set of ssid requests
        'Total Probes': pickle_data['Total Probes'],  # total number of network requests
    }

    return pd.Series(list(simple.values()), index=simple.keys())


def pickle_jar(pickles: iter, translator=pickle_to_series):
    """
    Makes an iterable collection of pickle data into a DataFrame
    :param translator: Function used to translate Pickle Data
    :param pickles: Iterable collection of dictionaries from pickles
    :return: Pandas DataFrame
    """
    result = []
    for pickle in pickles:
        result.append(translator(pickle))
    # Introspective Calculations
    result = pd.DataFrame(result).set_index('Interval')
    result['Congestion'] = result['Number Devices'] / np.percentile(result['Number Devices'].values,
                                                                    95)  # area congestion metric
    result['Congestion'] = result['Congestion'].apply(lambda x: x if x <= 1 else 1)
    return result


def get_vendor(mac: str):
    """
    Provided a MAC, return its vendor.
    REQUIRES INTERNET CONNECTION
    :param mac: MAC-Address
    :return: Vendor Name
    """

    # API base url,you can also use https if you need
    url = "http://macvendors.co/api/"

    request = urllib2.Request(url + mac, headers={'User-Agent': "API Browser"})
    response = urllib2.urlopen(request)
    # Fix: json object must be str, not 'bytes'
    reader = codecs.getreader("utf-8")
    obj = json.load(reader(response))
    # Print company name
    try:
        return str(obj['result']['company'])
    except KeyError:
        return None
