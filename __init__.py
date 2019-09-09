from add_folder_pair import add_new_folder_pair
from delete_folder_pair import view_and_delete_folder_pair
from view_folder_pair import view_and_sync_folders_pair_list


def init():
    while True:
        print("\n***** Folder Sync *****")
        print("1. Add New Folder Pair")
        print("2. Sync Folder Pair")
        print("3. Delete Folder Pair")
        print("0. Exit")
        ch = int(input("Enter Choice: "))
        if ch == 0:
            break
        if ch == 1:
            add_new_folder_pair()
        if ch == 2:
            view_and_sync_folders_pair_list()
        if ch == 3:
            view_and_delete_folder_pair()


if __name__ == '__main__':
    init()
