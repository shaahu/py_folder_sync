import tkinter as tk
from tkinter import filedialog

from helper import add_folder_pair_to_storage, display_folder_pair, check_sync


def add_new_folder_pair():
    pair_name = input("Give pair a name: ")
    print("Select Primary Folder: ")
    root = tk.Tk()
    root.withdraw()
    primary_path = filedialog.askdirectory()
    if primary_path:
        print("Your primary folder set to ==>: " + primary_path)
        print("Select Secondary Path: ")
        secondary_path = filedialog.askdirectory()
        print("Your secondary folder set to ==>: " + secondary_path)
        if secondary_path:
            res = add_folder_pair_to_storage(pair_name, primary_path, secondary_path)
            if res:
                print("Successfully added for sync list!")
            else:
                print("Failed to add!")
        else:
            print("Operation Cancelled!!!")
    else:
        print("Operation Cancelled!!!")