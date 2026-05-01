import unittest

from functions import *
from textnode import *
from htmlnode import *



class TestSplitNodeDelimiter(unittest.TestCase):
    def test_code_split(self):
       # print("Testing TextNode Split Function (1 Code Split).")
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        #print(node,"\n","\n",new_nodes)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ])
    def test_multi_node(self):
       # print("Testing Multi-Node splitting functionality.")
        nodes = [
        TextNode("This is text with a `code block` word", TextType.TEXT),
        TextNode("Oh Look, `Another code block` word already", TextType.TEXT),
        TextNode("This is already Code", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
        #print(nodes,"\n","\n",new_nodes)
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

class TestMardownExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.afakelink.net)"
        )
        self.assertListEqual([("link", "https://www.afakelink.net")], matches)

class TestSplitNodeImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_inverse_order(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) one is first and ![second image](https://i.imgur.com/3elNhQu.png) is next.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" one is first and ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" is next.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode("Theres no image in this node.",TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("Theres no image in this node.",TextType.TEXT)
            ],
            new_nodes,
        )

class TestSplitNodeLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_inverse_order(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) one is first and [second link](https://i.imgur.com/3elNhQu.png) is next.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" one is first and ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" is next.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_no_link(self):
        node = TextNode("Theres no link in this node.",TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Theres no link in this node.",TextType.TEXT)
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_one_of_each(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                 TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_only_bold_or_link(self):
        text = "This is a **text** with ![one image](fakeimage1.img)** and a bigger **![second image](biggerimage.jpeg)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is a ",TextType.TEXT),
                TextNode("text",TextType.BOLD),
                TextNode(" with ",TextType.TEXT),
                TextNode("one image",TextType.IMAGE,"fakeimage1.img"),
                TextNode(" and a bigger ",TextType.BOLD),
                TextNode("second image",TextType.IMAGE,"biggerimage.jpeg"),
            ],
            new_nodes,
        )

    def test_no_markdown_only_text(self):
        text = "There is no special text to convert."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("There is no special text to convert.",TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
