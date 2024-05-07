import os

from textnode import TextNode


def recursiveCopy():
    print(os.getcwd())


def recursiveDelete(path):
    if not os.path.exists(path):
        raise ValueError("Invalid Path")
    if os.path.isfile(path):
        os.remove(path)


if __name__ == "__main__":
    recursiveDelete("./public")
