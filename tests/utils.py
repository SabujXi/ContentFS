from os.path import join, abspath, dirname

BASE_DIR = dirname(abspath(__file__))
DATA_DIR = join(BASE_DIR, 'test_data')


def get_base_dir():
    return BASE_DIR


def get_data_dir():
    return DATA_DIR
