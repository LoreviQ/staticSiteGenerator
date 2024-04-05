from textnode import TextNode

if __name__ == "__main__":
    tn = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(tn.__repr__())
