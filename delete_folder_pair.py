from helper import display_folder_pair, delete_pair


def view_and_delete_folder_pair():
    if display_folder_pair():
        print(display_folder_pair())
        ch = int(input("Choose pair to delete: \n'0' to go back \n"))
        if ch == 0:
            pass
        else:
            delete_pair(str(ch))
    else:
        print("No pairs!")
