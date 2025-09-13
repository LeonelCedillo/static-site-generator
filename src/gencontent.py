import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def extract_title(md):
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f1, open(template_path, "r") as f2:
        markdown = f1.read()
        template = f2.read()

    parent_node = markdown_to_html_node(markdown)
    html = parent_node.to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)  
    final_html = final_html.replace('href="/', 'href="{basepath}').replace('src="/', 'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as out_file:
        out_file.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path) and from_path.endswith(".md"):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path, basepath)



