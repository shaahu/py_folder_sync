import operator
import os
from prettytable import PrettyTable

import json

from constant import PAIR_STORAGE_JSON, PAIR_NAME, PRIMARY_PATH, SECONDARY_PATH

MAX_CELL_LENGTH = 96


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


def get_files_list(loc):
    temp = []
    for path, subdirs, files in os.walk(loc):
        for name in files:
            temp.append(os.path.join(path.replace(loc, ""), name))
        for dir in subdirs:
            temp.append(os.path.join(path.replace(loc, ""), dir))
    return temp


def format_comment(comment, max_line_length):
    # accumulated line length
    ACC_length = 0
    words = comment.split(" ")
    formatted_comment = ""
    for word in words:
        if ACC_length + (len(word) + 1) <= max_line_length:
            formatted_comment = formatted_comment + word + " "
            ACC_length = ACC_length + len(word) + 1
        else:
            # append a line break, then the word and a space
            formatted_comment = formatted_comment + "\n" + word + " "
            ACC_length = len(word) + 1
    return formatted_comment


def ask_user(items_to_copy, items_to_delete):
    t = PrettyTable(
        ['Files to be copies to secondary folder', format_comment(", \n".join(items_to_copy), MAX_CELL_LENGTH)])
    t.add_row(
        ['Files to be deleted from secondary folder', format_comment(", \n".join(items_to_delete), MAX_CELL_LENGTH)])
    print(t)


def start_syncing(items_to_copy, items_to_delete, key):
    pass


def check_sync(key):
    data = get_storage_file()
    if key not in data:
        print("Invalid pair!")
    else:
        items_to_copy = list(
            set(get_files_list(data[key][PRIMARY_PATH])) - set(get_files_list(data[key][SECONDARY_PATH])))
        items_to_delete = list(
            set(get_files_list(data[key][SECONDARY_PATH])) - set(get_files_list(data[key][PRIMARY_PATH])))

        if not items_to_copy and not items_to_delete:
            print("Already Sync!")

        else:
            res = ask_user(items_to_copy, items_to_delete)
            if res:
                start_syncing(items_to_copy, items_to_delete, key)


if __name__ == '__main__':
    check_sync("5")
