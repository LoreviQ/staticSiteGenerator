import re

from textnode import TextNode


def split_textNode_delimiter(text_nodes, text_type):
    delimiter = {"bold": "**", "italic": "*", "code": "`"}[text_type]
    output = []
    for text_node in text_nodes:
        num_delimiters = text_node.text.count(delimiter)
        if num_delimiters == 0:
            output += [text_node]
        elif num_delimiters % 2 == 1:
            raise ValueError("Invalid markdown, formatted section not closed")
        else:
            split_text = text_node.text.split(delimiter)
            mode = False
            for text in split_text:
                if text == "":
                    continue
                if mode:
                    output += [TextNode(text, text_type)]
                else:
                    output += [TextNode(text, "text")]
                mode = not mode
    return output


def textNode_extract_markdown_images(text_nodes):
    output = []
    for text_node in text_nodes:
        text = text_node.text
        matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
        if not matches:
            output += [text_node]
            continue
        for match in matches:
            split_text = text.split(f"![{match[0]}]({match[1]})", maxsplit=1)
            if split_text[0]:
                output += [TextNode(split_text[0], "text")]
            output += [TextNode(match[0], "image", match[1])]
            text = split_text[1]
        if text:
            output += [TextNode(text, "text")]
    return output


def textNode_extract_markdown_links(text_nodes):
    output = []
    for text_node in text_nodes:
        text = text_node.text
        matches = re.findall(r"(?:[^!])\[(.*?)\]\((.*?)\)", text)
        if not matches:
            output += [text_node]
            continue
        for match in matches:
            split_text = text.split(f"[{match[0]}]({match[1]})", maxsplit=1)
            if split_text[0]:
                output += [TextNode(split_text[0], "text")]
            output += [TextNode(match[0], "link", match[1])]
            text = split_text[1]
        if text:
            output += [TextNode(text, "text")]
    return output


def text_to_textnode_markdown(text):
    node = [TextNode(text, "text")]
    node = textNode_extract_markdown_images(node)
    node = textNode_extract_markdown_links(node)
    node = split_textNode_delimiter(node, "bold")
    node = split_textNode_delimiter(node, "italic")
    node = split_textNode_delimiter(node, "code")
    return node


def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    output = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        output += [block]
    return output


def block_to_blocktype(block):
    if re.match(r"^(#{1,6} )", block):
        return "heading"
    if block[:3] == "```" and block[-3:] == "```":
        return "code"
    lines = block.split("\n")
    if all(line[0] == ">" for line in lines):
        return "quote"
    if all(re.match(r"^([*-] )", line) for line in lines):
        return "unordered_list"
    n = 1
    for line in lines:
        if line[:3] != f"{n}. ":
            return "paragraph"
        n += 1
    return "ordered_list"
