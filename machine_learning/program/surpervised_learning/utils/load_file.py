import configparser
import os
import errno

import pandas as pd


def load_config(config_file_name):
    config_dir = "../configs"
    config_path = os.path.join(config_dir, config_file_name)
    config_file = configparser.ConfigParser()
    if not os.path.exists(config_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
    config_file.read(config_path)

    return config_file


def load_data(data_file_name):
    data_dir = "../dataset"
    data_path = os.path.join(data_dir, data_file_name)
    try:
        data = pd.read_csv(data_path)
    except FileNotFoundError:
        print("FileNotFoundError")
    return data