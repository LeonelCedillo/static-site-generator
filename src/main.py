import os
import shutil
from textnode import TextNode, TextType


def main():
    source = os.path.abspath("static/")
    destination = os.path.abspath("public/")
    copy_source_to_destination(source, destination)


def delete_destination_content(destination_dir):
    for filename in os.listdir(destination_dir):
        file_path = os.path.join(destination_dir, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)


def copy_source_to_destination(source_dir, destination_dir):
    exists_src = os.path.exists(source_dir)
    exists_dest = os.path.exists(destination_dir)
    if not exists_src: 
        raise Exception("The source path does not exists.")
    if not exists_dest: 
        parent_dir = os.path.dirname(source_dir)
        new_path = os.path.join(parent_dir, "public")
        destination_dir = os.mkdir(new_path)
    delete_destination_content(destination_dir)
    src_to_dst_rec(source_dir, destination_dir)


def src_to_dst_rec(source_path, destination_path):
    for filename in os.listdir(source_path):
        file_path = os.path.join(source_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            shutil.copy(file_path, destination_path)
        if os.path.isdir(file_path):
            dest_path = os.path.join(destination_path, filename)
            src_to_dst_rec(file_path, dest_path)






main()
