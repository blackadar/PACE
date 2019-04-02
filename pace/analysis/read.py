"""
Handles data input to analysis
"""
import logging
import os

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
        logging.debug("Data Directory not found, creating it...")
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


def un_pickle(path):
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


def simple_pickle_jar(pickles: iter):
    """
    Makes an iterable collection of pickle data into a DataFrame
    :param pickles: Iterable collection of dictionaries from pickles
    :return: Pandas DataFrame
    """
    result = []
    for pickle in pickles:
        result.append(simple_series(pickle))
    return pd.DataFrame(result).set_index('Interval')


def simple_series(pickle_data: dict):
    """
    Translate Pickle Data into a Series with Simple Sizes
    :param pickle_data: Dictionary from pace.analysis.read.un_pickle
    :return: Pandas Series
    """
    simple = {
        'Interval': pickle_data['Interval'],
        'Devices': len(pickle_data['Devices']),
        'SSID Requests': len(pickle_data['SSID Requests']),
        'Total Probes': pickle_data['Total Probes'],
    }

    return pd.Series(list(simple.values()), index=simple.keys())
