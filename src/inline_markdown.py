from textnode import TextNode, TextType, text_node_to_html_node
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiter_type = {"`": TextType.CODE, "**": TextType.BOLD, "_": TextType.ITALIC}
    TYPE = delimiter_type[delimiter]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splitted_text = node.text.split(delimiter)
        if len(splitted_text) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(splitted_text)):
            if splitted_text[i] != "":
                if i % 2 == 0:
                    new_nodes.append(TextNode(splitted_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(splitted_text[i], TYPE))
    return new_nodes

    
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        markdown_images = extract_markdown_images(node.text) # [(image alt, image link), (same)]
        if len(markdown_images) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for image in markdown_images: # image = (image_alt, image_link)
            image_alt = image[0]
            image_link = image[1]
            splitted_text = node_text.split(f"![{image_alt}]({image_link})", 1) # ["text before pattern", "text after pattern"]
            if len(splitted_text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1])) # TextNode(text, text_type, url)
            node_text = splitted_text[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        markdown_links = extract_markdown_links(node.text) 
        if len(markdown_links) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for link in markdown_links: 
            link_text = link[0]
            link_link = link[1]
            splitted_text = node_text.split(f"[{link_text}]({link_link})", 1) 
            if len(splitted_text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1])) 
            node_text = splitted_text[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


