import unittest

from functions import *
from textnode import *
from htmlnode import *

###################################################################
##########            Tests for Inline Code            ############
###################################################################

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ])
    def test_multi_node(self):
        nodes = [
        TextNode("This is text with a `code block` word", TextType.TEXT),
        TextNode("Oh Look, `Another code block` word already", TextType.TEXT),
        TextNode("This is already Code", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
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

######################################################################################
#####################            Tests for Block Code            #####################
######################################################################################

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_excessive_newlines_blocks(self):
        md = """




So theres way too many new lines in this mark down



          There should only be two paragraph
blocks accepted.           




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "So theres way too many new lines in this mark down",
                "There should only be two paragraph\nblocks accepted."
            ],
        )

    def test_no_blocks_found(self):
        md = """




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,[],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_para_block(self):
        block = "This is just a simple paragraph"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.PARA,
        )

    def test_heading1_block(self):
        block = "# This is a heading block"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.HEAD,
        )
    def test_heading2_block(self):
        block = "## This is a heading block"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.HEAD,
        )
    def test_heading3_block(self):
        block = "### This is a heading block"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.HEAD,
        )
    def test_heading4_block(self):
        block = "#### This is a heading block"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.HEAD,
        )
    def test_heading5_block(self):
        block = "##### This is a heading block"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.HEAD,
        )
    def test_heading6_block(self):
        block = "###### This is a heading block"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.HEAD,
        )
    def test_heading7_block(self):
        block = "####### This is a heading block"
        b_type = block_to_block_type(block)
        self.assertNotEqual(
            b_type,
            BlockType.HEAD,
        )

    def test_code_block(self):
        block = "```\nThis is a code block\nsecond line of code\nthird line of code```"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.CODE,
        )
    def test_code_block_fail(self):
        block = "`\nThis is a code block\nsecond line of code\nthird line of code`"
        b_type = block_to_block_type(block)
        self.assertNotEqual(
            b_type,
            BlockType.CODE,
        )

    def test_quote_block(self):
        block = "> First Line of the Quote Block\n> Second Line\n> Third Line"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.QUOTE
        )
    def test_quote_block_fail(self):
        block = "> First Line of the Quote Block\n Second Line\n Third Line"
        b_type = block_to_block_type(block)
        self.assertNotEqual(
            b_type,
            BlockType.QUOTE
        )

    def test_unordered_list_block(self):
        block = "- First Item on List\n- Second Item\n- Third Item"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.UNLIST
        )
    def test_unordered_list_block_fail(self):
        block = "- First Item on List\n Second Item\n Third Item"
        b_type = block_to_block_type(block)
        self.assertNotEqual(
            b_type,
            BlockType.UNLIST
        )

    def test_ordered_list_block(self):
        block = "1. First Item on List\n2. Second Item\n3. Third Item"
        b_type = block_to_block_type(block)
        self.assertEqual(
            b_type,
            BlockType.ORDLIST
        )
    def test_ordered_list_block_fail(self):
        block = "1. First Item on List\n2. Second Item\n5. Third Item"
        b_type = block_to_block_type(block)
        self.assertNotEqual(
            b_type,
            BlockType.ORDLIST
        )


##################################################
##########   TESTS FOR BLOCKS TO HTML   ##########
##################################################

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )

    def test_all_blocks_test(self):
        md = """
### Heading Block (h3)

This is **bold text** inside of a paragraph

> Now we have
> a _quote block_
> to add

- Unordered List 1
- Unordered List 2

1. Ordered List 1
2. Ordered List 2

```
And _now_ we have some
code to **finish** us out
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading Block (h3)</h3><p>This is <b>bold text</b> inside of a paragraph</p><blockquote>Now we have a <i>quote block</i> to add</blockquote><ul><li>Unordered List 1</li><li>Unordered List 2</li></ul><ol><li>Ordered List 1</li><li>Ordered List 2</li></ol><pre><code>And _now_ we have some\ncode to **finish** us out\n</code></pre></div>"
        )

    def test_extract_title(self):
        md = """
# This is a Title  

A test Paragraph
"""
        title = extract_title(md)
        self.assertEqual(
            title, "This is a Title"
        )

    def test_extract_title_missing(self):
        md = """
No Title to extract  

A test Paragraph
"""
        
        self.assertRaises(Exception,extract_title,md)

    def test_extract_title_wrong_header(self):
        md = """
### Wrong Header  

A test Paragraph
"""
        
        self.assertRaises(Exception,extract_title,md)

    def test_extract_title_no_markdown(self):
        md = """



"""
        
        self.assertRaises(Exception,extract_title,md)


    def test_extract_title_text_before_title(self):
        md = """
A test Paragraph

# This is a Title 
"""
        title = extract_title(md)
        self.assertEqual(
            title, "This is a Title"
        )



if __name__ == "__main__":
    unittest.main()
