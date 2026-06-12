import re

from textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        splits = node.text.split(delimiter)
        for i in range(0, len(splits)):
            if i % 2 != 0:
                result.append(TextNode(splits[i], text_type))
            else:
                if splits[i] == "":
                    continue
                result.append(TextNode(splits[i], TextType.TEXT))
    return result


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            image_tuples = extract_markdown_images(node.text)
            text_list = node.text
            if len(image_tuples) == 0:
                result.append(node)
                continue
            for image in image_tuples:
                image_node = TextNode(image[0], TextType.IMAGE, image[1])
                text_list = text_list.split(
                    f"![{image_node.text}]({image_node.url})", 1
                )
                if text_list[0] != "":
                    result.append(TextNode(text_list[0], TextType.TEXT))
                result.append(image_node)
                text_list = text_list[1]
            if text_list != "":
                result.append(TextNode(text_list, TextType.TEXT))
    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            link_tuples = extract_markdown_links(node.text)
            text_list = node.text
            if len(link_tuples) == 0:
                result.append(node)
                continue
            for link in link_tuples:
                link_node = TextNode(link[0], TextType.LINK, link[1])
                text_list = text_list.split(f"[{link_node.text}]({link_node.url})", 1)
                if text_list[0] != "":
                    result.append(TextNode(text_list[0], TextType.TEXT))
                result.append(link_node)
                text_list = text_list[1]
            if text_list != "":
                result.append(TextNode(text_list, TextType.TEXT))
    return result
