from add_folder_pair import add_new_folder_pair
from view_folder_pair import view_folders_pair_list


def init():
    while True:
        print("Folder Sync")
        print("1. Add New Folder Pair")
        print("2. View Folder Pair")
        print("3. Delete Folder Pair")
        print("9. Exit")
        ch = int(input("Enter Choice: "))
        if ch == 9:
            break
        if ch == 1:
            add_new_folder_pair()
        if ch == 2:
            view_folders_pair_list()


if __name__ == '__main__':
    init()
