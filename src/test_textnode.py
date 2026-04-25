import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        print("Testing Equal TextNodes.\n",node,"\n",node2)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This one won't work", TextType.ITALIC_TEXT)
        print("Testing Not Equal TextNodes.\n",node,"\n",node2)
        self.assertNotEqual(node,node2)

    def test_noturl(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This one won't work", TextType.ITALIC_TEXT,"fancy URL")
        print("Testing Not Equal TextNodes w/ URL.\n",node,"\n",node2)
        self.assertNotEqual(node,node2)

    def test_url(self):
        node = TextNode("This one will work", TextType.BOLD_TEXT,"Matching URL")
        node2 = TextNode("This one will work", TextType.BOLD_TEXT,"Matching URL")
        print("Testing Equal TextNodes w/ URL.\n",node,"\n",node2)
        self.assertEqual(node,node2)




if __name__ == "__main__":
    unittest.main()