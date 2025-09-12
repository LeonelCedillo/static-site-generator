import os
from markdown_blocks import markdown_to_blocks, markdown_to_html_node
# from htmlnode import HTMLNode, LeafNode, ParentNode


# def extract_title(markdown):
#     blocks = markdown_to_blocks(markdown)
#     for block in blocks:
#         if block.startswith("# "):
#             return block.lstrip("#").strip()
#     raise Exception("No h1 found")

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()  # remove the "# " prefix
    raise Exception("No h1 found")

    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f1, open(template_path, "r") as f2:
        markdown = f1.read()
        template = f2.read()
    
    parent_node = markdown_to_html_node(markdown)
    html = parent_node.to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)        

    with open(dest_path, "w") as out_file:
        out_file.write(final_html)