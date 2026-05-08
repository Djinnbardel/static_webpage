import re
import shutil
import os

from enum import Enum
from textnode import *
from htmlnode import *


#############################
# Inline Markdown Functions #
#############################

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
    nodes = split_nodes_links(
        split_nodes_images(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text,TextType.TEXT)],
                            '**',TextType.BOLD),
                                '_',TextType.ITALIC),
                                    '`',TextType.CODE)))
    return nodes


####################
# Block Type Enums #
####################


class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNLIST = "unordered_list"
    ORDLIST = "ordered_list"


############################
# Block Markdown Functions #
############################

def markdown_to_blocks(markdown):
    temp = markdown.split("\n\n")
    blocks = []
    for x in range(0,len(temp)):
        if len(temp[x].strip()) == 0:
            continue
        else:
            blocks.append(temp[x].strip())
    return blocks

def block_to_block_type(block):
    if block.startswith(('# ','## ','### ','#### ','##### ','###### ')):
        return BlockType.HEAD

    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE

    if block.startswith('> '):
        templines = block.split('\n')
        counter = 0
        while counter < len(templines):
            if templines[counter].startswith('> '):
                counter += 1
            else:
                break
        if counter == len(templines):
            return BlockType.QUOTE

    if block.startswith('- '):
        templines = block.split('\n')
        counter = 0
        while counter < len(templines):
            if templines[counter].startswith('- '):
                counter += 1
            else:
                break
        if counter == len(templines):
            return BlockType.UNLIST

    if block.startswith('1. '):
        templines = block.split('\n')
        counter = 0
        while counter < len(templines):
            if templines[counter].startswith(f'{counter+1}. '):
                counter += 1
            else:
                break
        if counter == len(templines):
            return BlockType.ORDLIST

    return BlockType.PARA


################################################
############  Markdown to HTMLNode  ############
################################################

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    return children

def block_to_html_node(block):
    b_type = block_to_block_type(block)
    if b_type == BlockType.PARA:
        text = block.replace('\n',' ')
        children = text_to_children(text)
        return ParentNode("p",children)

    elif b_type == BlockType.HEAD:
        h_num = block.count('#',0,block.find(' '))
        try:
            text = block[h_num + 1:]
        except Exception:
            raise ValueError("Error: Heading malformed.")
        children = text_to_children(text)
        return ParentNode(f"h{h_num}",children)

    elif b_type == BlockType.QUOTE:
        lines = block.split('\n')
        cleaned = [line.removeprefix('>').lstrip() for line in lines]
        text = " ".join(cleaned)
        children = text_to_children(text)
        return ParentNode("blockquote",children)
    
    elif b_type == BlockType.UNLIST:
        lines = block.split('\n')
        listed = []
        for line in lines:
            text = line.removeprefix('-').lstrip()
            child = text_to_children(text)
            listed.append(ParentNode("li",child))
        return ParentNode("ul",listed)

    elif b_type == BlockType.ORDLIST:
        lines = block.split('\n')
        listed = []
        for line in lines:
            text = line.split('. ', 1)
            child = text_to_children(text[1])
            listed.append(ParentNode("li",child))
        return ParentNode("ol",listed)

    elif b_type == BlockType.CODE:
        code_node = TextNode(block.strip('`').lstrip(),TextType.CODE)
        return ParentNode("pre",[text_node_to_html_node(code_node)])


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    main_node_children = []
    for block in blocks:
       main_node_children.append(block_to_html_node(block))
    return ParentNode("div",main_node_children)
       

#************************************************#
#****           Website Functions            ****#
#************************************************#

def copy_files_over(source_dir,dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    src_list = os.listdir(source_dir)
    for item in src_list:
        if os.path.isfile(os.path.join(source_dir,item)):
            shutil.copy(os.path.join(source_dir,item),dest_dir)
        else:
            new_dir = os.path.join(dest_dir,item)
            os.mkdir(new_dir)
            copy_files_over(os.path.join(source_dir,item),new_dir)




