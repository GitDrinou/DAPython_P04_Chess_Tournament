import json


def read_file(path_file):
    """Read a file and return a list"""
    with open(path_file, "r") as f:
        data = json.load(f)
        if data:
            return data
        else:
            return None


def write_file(path_file, data):
    """Write data to a file"""
    with open(path_file, "w") as f:
        json.dump(data, f, indent=4)
