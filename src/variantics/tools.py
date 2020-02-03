import os


def ensure_folder_exists(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
