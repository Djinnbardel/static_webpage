import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):

    ###HTMLNode Tests
    
    def test_nodeprint(self):
        node = HTMLNode("Has Tag","This Node has no children or props")
       # print("Testing HTMLNodes.")
       # print(node,'\n')
        self.assertEqual(repr(node), "HTMLNode(Has Tag,This Node has no children or props,None,)")

    def test_nodeURL(self):
        node2 = HTMLNode("Has Tag","This Node has no children",None,{"href": "https://nottasite.com", "target": "_not_applicable", "third": "_a_Test"})
       # print("Testing HTMLNodes with Props.")
       # print(node2,'\n')
        self.assertEqual(repr(node2), 'HTMLNode(Has Tag,This Node has no children,None, href="https://nottasite.com" target="_not_applicable" third="_a_Test")')    


class TestLeafNode(unittest.TestCase):
    
    ###LeafNode Tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
       # print("Testing LeafNode [No Props]")
       # print(node,'\n')
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "What is this Monster!", {"href": "www.monsterwow.net"})
       # print("Testing LeafNode [With Props]")
       # print(node,'\n')
        self.assertEqual(node.to_html(), '<a href="www.monsterwow.net">What is this Monster!</a>')
    
    def test_leaf_to_html_x(self):
        node = LeafNode(None, "Oh My Lord its Just Text.")
       # print("Testing LeafNode [No Tag]")
       # print(node,'\n')
        self.assertEqual(node.to_html(), "Oh My Lord its Just Text.")


class TestParentNode(unittest.TestCase):

    ###ParentNode Tests

    def test_no_tag(self):
       # print("Testing Parent Node w/ no Tag\n")
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaisesRegex(ValueError, "Error: ParentNode must have a tag")

    def test_to_html_with_children(self):
       # print("Testing Parent Node w/ No Children")
        parent_node = ParentNode("div", None)
        self.assertRaisesRegex(ValueError, "Error: Child nodes missing")

    def test_to_html_with_children(self):
       # print("Testing Parent Node w/ Children\n")
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
       # print("Testing ParentNode w/ GrandChildren\n")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_multidepth(self):
       # print("Testing ParentNode w/ Multidepth\n")
        grandchild_node = LeafNode("b", "grandchild")
        cousin_node = LeafNode("p", "cousin")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node,cousin_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span><p>cousin</p></div>") 



if __name__ == "__main__":
    unittest.main()