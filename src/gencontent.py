import os
from markdown_blocks import markdown_to_html_node


def extract_title(md):
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
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

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as out_file:
        out_file.write(final_html)

