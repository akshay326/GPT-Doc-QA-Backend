import json
import pickle


def pickle_dump(obj, filepath):
    """
    Pickle dump object to filepath
    """
    pickle.dump(obj, open(filepath, 'wb'))


def pickle_load(filepath):
    """
    Pickle load object from filepath
    """
    return pickle.load(open(filepath, 'rb'))


def json_dump(obj, filepath):
    """
    JSON dump object to filepath
    """
    with open(filepath, 'w') as f:
        json.dump(obj, f)


def json_load(filepath):
    """
    JSON load object from filepath
    """
    with open(filepath, 'r') as f:
        return json.load(f)
