from block_parse import block_to_html_node
from htmlnode import HTMLNode, ParentNode


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_nodes.append(block_to_html_node(block))
    return ParentNode("div", html_nodes)


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        html_node = block_to_html_node(block)
        if html_node.tag == "h1":
            return html_node.to_html()
    raise Exception("no h1 title")


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block == "":
            continue
        result.append(block.strip())
    return result
