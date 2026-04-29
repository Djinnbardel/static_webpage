from textnode import *
from htmlnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Error: {node} text does not have corresponding closing delimiters.")
        else:
            textsplit = node.text.split(delimiter)
            tempnodes = []
            for x in range(0,len(textsplit)):
                if x % 2 == 0:
                    if textsplit[x] == "":
                        continue
                    else:
                        tempnode = TextNode(textsplit[x],TextType.TEXT)
                        tempnodes.append(tempnode)
                else:
                    tempnode = TextNode(textsplit[x],text_type)
                    tempnodes.append(tempnode)
            new_nodes.extend(tempnodes)
    return new_nodes


