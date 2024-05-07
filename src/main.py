import os
import shutil

from textnode import TextNode


def copy_directory(src, dst):
    if not os.path.exists(dst):
        recursive_delete(dst)
    recursive_copy(src, dst, "")


def recursive_copy(src, dst, sub_path):
    s_path = os.path.join(src, sub_path)
    d_path = os.path.join(dst, sub_path)
    if not os.path.exists(s_path):
        raise ValueError("Invalid Path")
    if os.path.isdir(s_path):
        os.mkdir(d_path)
        dir_entries = os.listdir(s_path)
        for entry in dir_entries:
            recursive_copy(src, dst, os.path.join(sub_path, entry))
    if os.path.isfile(s_path):
        shutil.copy(s_path, d_path)


def recursive_delete(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        dir_entries = os.listdir(path)
        for entry in dir_entries:
            recursive_delete(os.path.join(path, entry))
        os.rmdir(path)
    raise ValueError("Invalid Path")


if __name__ == "__main__":
    copy_directory("./static", "./public")
