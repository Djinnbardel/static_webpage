import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This one won't work", TextType.ITALIC)
        self.assertNotEqual(node,node2)

    def test_noturl(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This one won't work", TextType.ITALIC,"fancy URL")
        self.assertNotEqual(node,node2)

    def test_url(self):
        node = TextNode("This one will work", TextType.BOLD,"Matching URL")
        node2 = TextNode("This one will work", TextType.BOLD,"Matching URL")
        self.assertEqual(node,node2)

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a BOLD text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a BOLD text node")
    
    def test_italic(self):
        node = TextNode("This is an Italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an Italic text node")
    
    def test_code(self):
        node = TextNode("This is a [code] node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a [code] node")

    def test_link(self):
        node = TextNode("This is a url node", TextType.LINK,"www.coolurl.net")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a url node")
        self.assertEqual(html_node.props, {"href": "www.coolurl.net"})
    
    def test_image(self):
        node = TextNode("This is an image node.", TextType.IMAGE, "httpss//www.picture.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "httpss//www.picture.org", "alt": "This is an image node."})
    
    def test_type_error(self):
        node = TextNode("Oh No Error Raised.", "ErrorType")
        self.assertRaises(ValueError, text_node_to_html_node,node)
        
        
        
        




if __name__ == "__main__":
    unittest.main()