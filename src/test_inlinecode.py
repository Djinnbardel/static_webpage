import unittest

from functions import *
from textnode import *
from htmlnode import *



class TestSplitNodeDelimiter(unittest.TestCase):
    def test_code_split(self):
        print("Testing TextNode Split Function (1 Code Split).")
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        print(node,"\n","\n",new_nodes)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ])
    def test_multi_node(self):
        print("Testing Multi-Node splitting functionality.")
        nodes = [
        TextNode("This is text with a `code block` word", TextType.TEXT),
        TextNode("Oh Look, `Another code block` word already", TextType.TEXT),
        TextNode("This is already Code", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
        print(nodes,"\n","\n",new_nodes)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        TextNode("Oh Look, ", TextType.TEXT),
        TextNode("Another code block", TextType.CODE),
        TextNode(" word already", TextType.TEXT),
        TextNode("This is already Code", TextType.CODE),
        ])

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
    



