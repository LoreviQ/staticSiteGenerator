import os

from textnode import TextNode


def recursive_copy(copy, destination):
    if not os.path.exists(destination):
        recursive_delete(destination)


def recursive_delete(path):
    if not os.path.exists(path):
        raise ValueError("Invalid Path")
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        dir_entries = os.listdir(path)
        for entry in dir_entries:
            recursive_delete(os.path.join(path, entry))
        os.rmdir(path)
    raise ValueError("Invalid Path")


if __name__ == "__main__":
    recursive_copy("./static", "./public")
