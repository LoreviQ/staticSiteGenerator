import os

from textnode import TextNode


def recursiveCopy():
    print(os.getcwd())


def recursiveDelete(path):
    print(os.path.exists(path))


if __name__ == "__main__":
    recursiveDelete("./public")
