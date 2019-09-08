import operator
import os
from prettytable import PrettyTable

import json

from constant import PAIR_STORAGE_JSON, PAIR_NAME, PRIMARY_PATH, SECONDARY_PATH


def create_file_if_not_exist():
    try:
        if not os.path.exists(PAIR_STORAGE_JSON):
            open(PAIR_STORAGE_JSON, "w")
    except Exception as e:
        print(e)


def get_storage_file():
    return json.loads(open(PAIR_STORAGE_JSON, "r").read())


def write_to_storage(incoming):
    create_file_if_not_exist()
    try:
        with open(PAIR_STORAGE_JSON, "r") as f:
            data = json.load(f)
        data.update(incoming)
        with open(PAIR_STORAGE_JSON, 'w') as f:
            json.dump(data, f)
    except:
        with open(PAIR_STORAGE_JSON, 'w') as f:
            json.dump(incoming, f)


def generatekey():
    key_list = list()
    count = 1
    try:
        for key in get_storage_file():
            key_list.append(int(key))
    except Exception as e:
        print(e)
        return count
    for i in range(len(key_list)):
        if count in key_list:
            count += 1
        else:
            break
    return count


def add_folder_pair_to_storage(pair_name, primary_path, secondary_path):
    try:
        element = {PAIR_NAME: pair_name, PRIMARY_PATH: primary_path, SECONDARY_PATH: secondary_path}
        path_dict = {generatekey(): element}
        write_to_storage(path_dict)
        return True
    except Exception as e:
        print(e)
        return False


def display_pair_folders():
    pairs = get_storage_file()
    t = PrettyTable(['#', 'Name', 'Primary', 'Secondary'])
    for key in pairs:
        t.add_row([key, pairs[key][PAIR_NAME], pairs[key][PRIMARY_PATH], pairs[key][SECONDARY_PATH]])
    return t.get_string(sort_key=operator.itemgetter(1, 0), sortby="#")


def check_sync(key):
    data = get_storage_file()
    if key not in data:
        print("Invalid pair!")
    else:
        primary = data[key][PRIMARY_PATH]
        secondary = data[key][SECONDARY_PATH]
        print(primary)
        print(secondary)


if __name__ == '__main__':
    check_sync("1")
