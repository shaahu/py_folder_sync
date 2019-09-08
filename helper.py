import errno
import operator
import os
import shutil

from prettytable import PrettyTable

import json
from shutil import copy, rmtree, copyfile

from constant import PAIR_STORAGE_JSON, PAIR_NAME, PRIMARY_PATH, SECONDARY_PATH

MAX_CELL_LENGTH = 96


def create_file_if_not_exist():
    try:
        if not os.path.exists(PAIR_STORAGE_JSON):
            open(PAIR_STORAGE_JSON, "w")
    except Exception as e:
        print(e)


def check_if_path_exist(path):
    return os.path.exists(path)


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


def display_folder_pair():
    pairs = get_storage_file()
    t = PrettyTable(['#', 'Name', 'Primary', 'Secondary'])
    if pairs:
        for key in pairs:
            t.add_row([key, pairs[key][PAIR_NAME], pairs[key][PRIMARY_PATH], pairs[key][SECONDARY_PATH]])
            return t.get_string(sort_key=operator.itemgetter(1, 0), sortby="#")
    else:
        return []


def get_files_list(loc):
    temp = []
    for path, subdirs, files in os.walk(loc):
        for name in files:
            temp.append(os.path.join(path.replace(loc, ""), name))
        for dir in subdirs:
            temp.append(os.path.join(path.replace(loc, ""), dir))
    return temp


def ask_user(items_to_copy, items_to_delete):
    t = PrettyTable(["Operation", "Files"])
    t.add_row(['Files to be copies to secondary folder: ' + str(len(items_to_copy)), ", \n".join(items_to_copy)])
    t.add_row(['--------------------------------------', '---------------'])
    t.add_row(['Files to be deleted from secondary folder: ' + str(len(items_to_delete)), ", \n".join(items_to_delete)])
    print(t)
    print("1. Full Sync")
    print("2. Copy Only")
    print("3. Delete Only")
    print("4. Cancel")
    return int(input("Choose your sync operation: "))


def copytree(src, dst, total_item, flag):
    global count, counter
    if flag:
        count = 1
        counter = []
    for x in total_item:
        if os.path.isfile(src + x):
            counter.append(x)
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, total_item, False)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)
                print("Copying (" + str(count) + " of " + str(len(counter)) + ") ==> " + item)
                count += 1


def delete_file(path, item):
    item = item.replace("\\", "/")
    if check_if_path_exist(path + "/" + item):
        try:
            os.remove(path + "/" + item)
        except:
            rmtree(path + "/" + item)


def start_full_syncing(items_to_copy, items_to_delete, key):
    data = get_storage_file()
    src_path = data[key][PRIMARY_PATH]
    dest_path = data[key][SECONDARY_PATH]
    if items_to_copy:
        copytree(src_path, dest_path, items_to_copy, True)
    for item in items_to_delete:
        delete_file(dest_path, item)
    print("Syncing Successful")


def copy_only(items_to_copy, key):
    data = get_storage_file()
    src_path = data[key][PRIMARY_PATH]
    dest_path = data[key][SECONDARY_PATH]
    if items_to_copy:
        copytree(src_path, dest_path, items_to_copy, True)
        print("Syncing Successful")


def delete_only(items_to_delete, key):
    data = get_storage_file()
    dest_path = data[key][SECONDARY_PATH]
    for item in items_to_delete:
        delete_file(dest_path, item)
    print("Syncing Successful")


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
            if res == 1:
                start_full_syncing(items_to_copy, items_to_delete, key)
            if res == 2:
                copy_only(items_to_copy, key)
            if res == 3:
                delete_only(items_to_delete, key)
            if res == 4:
                print("Operation Aborted!")
                pass


def delete_json_element(key):
    with open(PAIR_STORAGE_JSON) as data_file:
        data = json.load(data_file)

    if key in data:
        yn = input("Are you sure you want delete pair (" + data[key][PAIR_NAME] + ") yes/no? ")
        print(yn)
        if yn == 'y' or yn == 'yes':
            del data[key]
            with open(PAIR_STORAGE_JSON, 'w') as data_file:
                json.dump(data, data_file)
                print(key + " deleted")
        if yn == 'n' or yn == 'no':
            print("Aborted!")
            pass
    else:
        print("Pair: " + key + " not found!")


def delete_pair(key):
    data = get_storage_file()
    if key not in data:
        print("Invalid pair!")
    else:
        delete_json_element(key)
