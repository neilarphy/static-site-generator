from site_generation import copy_dir, generate_pages_recursive
from textnode_enhancements import extract_markdown_images



def main():
    source_dir = 'static'
    destination_dir = 'public'
    content_dir = 'content'
    tmplt = 'template.html'
    file_dst = 'public'
    #testing new name
    copy_dir(source_dir, destination_dir)
    generate_pages_recursive(content_dir, tmplt, file_dst)


main()