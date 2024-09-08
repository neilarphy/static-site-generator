import os
import shutil
from textnode_enhancements import extract_title, markdown_to_html_node

def copy_dir(src, dst):
    """
    Recursively copy all contentes from src to dst, 
    ensuring dst is clean
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)


        if os.path.isdir(src_path):
            copy_dir(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
            #print(f'Copied {src_path} to {dst_path}')

def generate_page(from_path, template_path, dst_path):
    #print(f'Generating page from {from_path} to {dst_path} using {template_path}')

    with open(from_path, 'r') as file:
        markdown_text = file.read()

    with open(template_path, 'r') as file:
        template_text = file.read()

    title = extract_title(markdown_text)
    content = markdown_to_html_node(markdown_text).to_html()

    page_text = template_text.replace('{{ Title }}', title).replace('{{ Content }}', content)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with open(dst_path, 'w') as f:
        f.write(page_text)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    #print(f"Processing directory: {dir_path_content}")
    os.makedirs(dest_dir_path, exist_ok=True)
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        rel_path = os.path.relpath(item_path, dir_path_content)
        dest_path = os.path.join(dest_dir_path, rel_path)

        #print(f"Processing item: {item_path}")
        if os.path.isfile(item_path):
            if item.endswith('.md'):
                #print(f"Generating page for: {item_path}")
                dest_html_path = os.path.splitext(dest_path)[0] + '.html'
                generate_page(item_path, template_path, dest_html_path)
        else:
            #print(f"Found directory: {item_path}")
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(item_path, template_path, dest_path)