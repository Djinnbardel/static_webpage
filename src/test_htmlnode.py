import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    node = HTMLNode("Has Tag","This Node has no children or props")
    node2 = HTMLNode("Has Tag","This Node has no children",None,{"href": "https://nottasite.com", "target": "_not_applicable", "third": "_a_Test"})
    
    def test_nodeprint(self):
        print("Testing HTMLNodes.")
        print(self.node)
        self.assertTrue(self.node, "HTMLNode(Has Tag,This Node has no children or props,None,)")

    def test_nodeURL(self):
        print("Testing HTMLNodes with Props.")
        print(self.node2)
        self.assertTrue(self.node2, 'HTMLNode(Has Tag,This Node has no children,None, href="https://nottasite.com" target="_not_applicable" third="_a_Test")')    



if __name__ == "__main__":
    unittest.main()