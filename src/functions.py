import re

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

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return links

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
            continue

        sections = []
        temptext = node.text
        for x in range(0,len(links)):
            temp = temptext.split(f"[{links[x][0]}]({links[x][1]})",1)
            sections.append(temp[0])
            sections.append(f"[{links[x][0]}]({links[x][1]})")
            if x == len(links)-1:
                sections.append(temp[1])
            else:
                temptext = temp[1]
        
        tempnodes = []
        for part in range(0,len(sections)):
            if part % 2 == 0:
                if sections[part] == "":
                    continue
                else:
                    tempnode = TextNode(sections[part],TextType.TEXT)
                    tempnodes.append(tempnode)
            else:
                tempnode = TextNode(links[part//2][0],TextType.LINK,links[part//2][1])
                tempnodes.append(tempnode)
        new_nodes.extend(tempnodes)
    return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
            continue

        sections = []
        temptext = node.text
        for x in range(0,len(images)):
            temp = temptext.split(f"![{images[x][0]}]({images[x][1]})",1)
            sections.append(temp[0])
            sections.append(f"![{images[x][0]}]({images[x][1]})")
            if x == len(images)-1:
                sections.append(temp[1])
            else:
                temptext = temp[1]
        
        tempnodes = []
        for part in range(0,len(sections)):
            if part % 2 == 0:
                if sections[part] == "":
                    continue
                else:
                    tempnode = TextNode(sections[part],TextType.TEXT)
                    tempnodes.append(tempnode)
            else:
                tempnode = TextNode(images[part//2][0],TextType.IMAGE,images[part//2][1])
                tempnodes.append(tempnode)
        new_nodes.extend(tempnodes)
    return new_nodes


def text_to_textnodes(text):
    nodes = split_nodes_links(split_nodes_images(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text,TextType.TEXT)],'**',TextType.BOLD),'_',TextType.ITALIC),'`',TextType.CODE)))
    return nodes
    
        
