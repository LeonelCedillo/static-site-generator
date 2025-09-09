from textnode import TextNode, TextType, text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiter_type = {"`": TextType.CODE, "**": TextType.BOLD, "_": TextType.ITALIC}
    TYPE = delimiter_type[delimiter]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) < 2:
            raise Exception("Invalid Markdown syntax")
        splitted_text = node.text.split(delimiter)
        for i in range(len(splitted_text)):
            if splitted_text[i] != "":
                if i % 2 == 0:
                    new_nodes.append(TextNode(splitted_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(splitted_text[i], TYPE))
    return new_nodes

    