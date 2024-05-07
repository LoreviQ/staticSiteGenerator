import os

from textnode import TextNode


def recursiveCopy(copy, destination):
    if not os.path.exists(destination):
        recursiveDelete(destination)


def recursiveDelete(path):
    if not os.path.exists(path):
        raise ValueError("Invalid Path")
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        dir_entries = os.listdir(path)
        for entry in dir_entries:
            recursiveDelete(os.path.join(path, entry))
        os.rmdir(path)
    raise ValueError("Invalid Path")


if __name__ == "__main__":
    recursiveCopy("./static", "./public")
