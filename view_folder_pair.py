from helper import display_pair_folders, check_sync


def view_folders_pair_list():
    print(display_pair_folders())
    ch = int(input("Choose pair: "))
    check_sync(ch)