from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline_parse import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_html_node(block: str) -> HTMLNode:
    if block_to_block_type(block) == BlockType.PARAGRAPH:
        return paragraph_block_to_html_node(block)
    if block_to_block_type(block) == BlockType.HEADING:
        return heading_block_to_html_node(block)
    if block_to_block_type(block) == BlockType.CODE:
        return code_block_to_html_node(block)
    if block_to_block_type(block) == BlockType.QUOTE:
        return quote_block_to_html_node(block)
    if block_to_block_type(block) == BlockType.UNORDERED_LIST:
        return unordered_list_block_to_html_node(block)
    if block_to_block_type(block) == BlockType.ORDERED_LIST:
        return ordered_list_block_to_html_node(block)
    else:
        print(block)
        raise Exception("unknown block type")


def paragraph_block_to_html_node(block: str) -> HTMLNode:
    if block_to_block_type(block) != BlockType.PARAGRAPH:
        raise Exception("Not paragraph block")
    block = block.replace("\n", " ")
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    paragraph_node = ParentNode("p", html_nodes)
    return paragraph_node


def heading_block_to_html_node(block: str) -> HTMLNode:
    if block_to_block_type(block) != BlockType.HEADING:
        raise Exception("Not heading block")
    title = 0
    for i in range(6):
        if block[i] == "#":
            title += 1
        else:
            break
    block = block[title + 1 :]
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    heading_node = ParentNode(f"h{title}", html_nodes)
    return heading_node


def code_block_to_html_node(block: str) -> HTMLNode:
    if block_to_block_type(block) != BlockType.CODE:
        raise Exception("Not code block")
    block = block[4:-3]
    html_nodes = [text_node_to_html_node(TextNode(block, TextType.CODE))]
    code_node = ParentNode("pre", html_nodes)
    return code_node


def quote_block_to_html_node(block: str) -> HTMLNode:
    if block_to_block_type(block) != BlockType.QUOTE:
        raise Exception("Not quote block")
    new_block = ""
    for line in block.split("\n"):
        new_block += line[2:]
    text_nodes = text_to_textnodes(new_block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    quote_node = ParentNode("blockquote", html_nodes)
    return quote_node


def ordered_list_block_to_html_node(block: str) -> HTMLNode:
    if block_to_block_type(block) != BlockType.ORDERED_LIST:
        raise Exception("Not ordered list block")
    new_block = ""
    for line in block.split("\n"):
        new_block += "<li>" + line[3:] + "</li>"
    text_nodes = text_to_textnodes(new_block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    ordered_list_node = ParentNode("ol", html_nodes)
    return ordered_list_node


def unordered_list_block_to_html_node(block: str) -> HTMLNode:
    if block_to_block_type(block) != BlockType.UNORDERED_LIST:
        raise Exception("Not unordered list block")
    new_block = ""
    for line in block.split("\n"):
        new_block += "<li>" + line[2:] + "</li>"
    text_nodes = text_to_textnodes(new_block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    ordered_list_node = ParentNode("ul", html_nodes)
    return ordered_list_node


def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block[:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE
    lines = block.split("\n")
    quote = True
    unordered = True
    for line in lines:
        if line[0] != ">":
            quote = False
        if line[:2] != "- ":
            unordered = False
    if quote is True:
        return BlockType.QUOTE
    if unordered is True:
        return BlockType.UNORDERED_LIST
    ordered = True
    for i in range(len(lines)):
        if lines[i][: ((i + 1) // 10) + 3] != f"{i + 1}. ":
            ordered = False
    if ordered is True:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
