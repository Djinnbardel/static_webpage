import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):

    ###HTMLNode Tests
    
    def test_nodeprint(self):
        node = HTMLNode("Has Tag","This Node has no children or props")
        print("Testing HTMLNodes.")
        print(node)
        self.assertEqual(repr(node), "HTMLNode(Has Tag,This Node has no children or props,None,)")

    def test_nodeURL(self):
        node2 = HTMLNode("Has Tag","This Node has no children",None,{"href": "https://nottasite.com", "target": "_not_applicable", "third": "_a_Test"})
        print("Testing HTMLNodes with Props.")
        print(node2)
        self.assertEqual(repr(node2), 'HTMLNode(Has Tag,This Node has no children,None, href="https://nottasite.com" target="_not_applicable" third="_a_Test")')    


class TestLeafNode(unittest.TestCase):
    
    ###LeafNode Tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        print("Testing LeafNode [No Props]")
        print(node)
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "What is this Monster!", {"href": "www.monsterwow.net"})
        print("Testing LeafNode [With Props]")
        print(node)
        self.assertEqual(node.to_html(), '<a href="www.monsterwow.net">What is this Monster!</a>')
    
    def test_leaf_to_html_x(self):
        node = LeafNode(None, "Oh My Lord its Just Text.")
        print("Testing LeafNode [No Tag]")
        print(node)
        self.assertEqual(node.to_html(), "Oh My Lord its Just Text.")

if __name__ == "__main__":
    unittest.main()