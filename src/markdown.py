import re

from htmlnode import ParentNode
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


def block_to_HTMLNode(block):
    children = []
    match block_to_blocktype(block):
        case "paragraph":
            block = block.replace("\n", " ")
            text_nodes = text_to_textnode_markdown(block)
            for text_node in text_nodes:
                children += [text_node.to_html_node()]
            return ParentNode("p", children)
        case "heading":
            heading_tier = 0
            for char in block:
                if char == "#":
                    heading_tier += 1
                else:
                    break
            block = block[heading_tier + 1 :]
            text_nodes = text_to_textnode_markdown(block)
            for text_node in text_nodes:
                children += [text_node.to_html_node()]
            return ParentNode(f"h{heading_tier}", children)
        case "code":
            text_nodes = text_to_textnode_markdown(block[4:-3])
            for text_node in text_nodes:
                children += [text_node.to_html_node()]
            return ParentNode("pre", [ParentNode("code", children)])
        case "quote":
            lines = block.split("\n")
            block = ""
            for line in lines:
                block += line[1:] + " "
            text_nodes = text_to_textnode_markdown(block)
            for text_node in text_nodes:
                children += [text_node.to_html_node()]
            return ParentNode("blockquote", children)
        case "unordered_list":
            lines = block.split("\n")
            list_items = []
            for line in lines:
                children = []
                line = line[2:]
                line_nodes = text_to_textnode_markdown(line)
                for line_node in line_nodes:
                    children += [line_node.to_html_node()]
                list_items += [ParentNode("li", children)]
            return ParentNode("ul", list_items)
        case "ordered_list":
            lines = block.split("\n")
            list_items = []
            for line in lines:
                children = []
                line = line[3:]
                line_nodes = text_to_textnode_markdown(line)
                for line_node in line_nodes:
                    children += [line_node.to_html_node()]
                list_items += [ParentNode("li", children)]
            return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        children += [block_to_HTMLNode(block)]
    return ParentNode("div", children)
