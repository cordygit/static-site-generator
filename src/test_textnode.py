import unittest

from inline_parse import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text(self):
        node = text_to_textnodes("""
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

            """)
        html_node = text_node_to_html_node(node[0])
        self.assertEqual(html_node.tag, None)


if __name__ == "__main__":
    unittest.main()
