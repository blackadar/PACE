"""
Handles data input to analysis
"""
import os


def check_create_data():
    """
    Check for the data/ directory.
    Create it if it does not exist.
    :return:
    """
    dirs = os.listdir(os.getcwd())
    if 'data' not in dirs:
        print("[ ] Creating data directory.")
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
    os.remove(path)
