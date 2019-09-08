from helper import display_folder_pair, check_sync


def view_and_sync_folders_pair_list():
    if display_folder_pair():
        print(display_folder_pair())
        ch = int(input("Choose pair to sync: \n'0' to go back \n"))
        if ch == 0:
            pass
        else:
            check_sync(str(ch))
    else:
        print("No pairs!")
