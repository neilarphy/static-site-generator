import re
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    node_types = [
        "text",
        "bold",
        "italic",
        "code",
        "link",
        "image"
    ]

    if not isinstance(text_node, TextNode):
        raise TypeError("The provided node is not a TextNode")
    if text_node.text_type not in node_types:
        raise TypeError("Text node provided is from incorrect type")

    match text_node.text_type:
        case "text":
            return LeafNode(text_node.text, None, None)
        case "bold":
            return LeafNode(text_node.text, "b", None)
        case "italic":
            return LeafNode(text_node.text, "i", None)
        case "code":
            return LeafNode(text_node.text, "code", None)
        case "link":
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case "image":
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []
    #print(f"Splitting text: '{old_nodes[0].text}' with delimiter: {delimiter}")
   
    for node in old_nodes:
        if node.text_type == "text":
            text = node.text
            split_text = text.split(delimiter)
            
            if len(split_text) % 2 == 0:
                raise Exception(f"Mismatched delimiter in text: '{text}'")

            for idx, piece in enumerate(split_text):
                if idx % 2 == 0:
                    if piece:
                        result_nodes.append(TextNode(piece, "text"))
                else:
                    if piece:
                        result_nodes.append(TextNode(piece, text_type))
        else:
            result_nodes.append(node)
    
    return result_nodes


def extract_markdown_images(text):
    image_pattern = r'!\[(.*?)\]\((.*?)\)'
    return re.findall(image_pattern, text)

def extract_markdown_links(text):  
    link_pattern = r'\[(.*?)\]\((.*?)\)'
    return re.findall(link_pattern, text)

def split_nodes_image(old_nodes):
    result_nodes = []
    
    for node in old_nodes:
        text = str(node.text)
        if text == "":
            continue
        #print(f"Passing this text to extract_markdown_images: {text}")
        extracted_images = extract_markdown_images(text)
        #print(f'Extracted images: {extracted_images}')
        if extracted_images == []:
            result_nodes.append(node)
        else:
            for image in extracted_images:
                alt_text, url = image
                split_text = text.split(f'![{alt_text}]({url})', 1)
                result_nodes.append(TextNode(split_text[0], 'text'))
                result_nodes.append(TextNode(alt_text, 'image', url))
                text = split_text[1]
            if split_text[1] and not split_text[1] == "":
                result_nodes.append(TextNode(split_text[1], 'text'))

    return result_nodes

def split_nodes_link(old_nodes):

    result_nodes = []
    
    for node in old_nodes:
        text = str(node.text)
        if text == "":
            continue
        extracted_links = extract_markdown_links(text)

        if extracted_links == []:
            result_nodes.append(node)
        else:
            for link in extracted_links:
                alt_text, url = link
                split_text = text.split(f'[{alt_text}]({url})', 1)
                result_nodes.append(TextNode(split_text[0], 'text'))
                result_nodes.append(TextNode(alt_text, 'link', url))
                text = split_text[1]
            if split_text[1] and not split_text[1] == "":
                result_nodes.append(TextNode(split_text[1], 'text'))

    return result_nodes

'''
    def text_to_textnodes(text):
        nodes = [TextNode(text, "text")]
        resulting_nodes = []

        splitting_functions = [
            split_nodes_image,
            split_nodes_link,
            lambda nodes: split_nodes_delimiter(nodes, "**", "bold"),
            lambda nodes: split_nodes_delimiter(nodes, "*", "italic"),
            lambda nodes: split_nodes_delimiter(nodes, "`", "code")
        ]
        print(f'Current node {nodes}')
        while nodes:
            node = nodes.pop(0)
            current_nodes = [node]
            print(f'Current node {current_nodes}')
            for split_fnc in splitting_functions:
                current_nodes = split_fnc(current_nodes)
            
            resulting_nodes.extend(current_nodes)
        
        return resulting_nodes
'''

def markdown_to_blocks(markdown):
    blocks = re.split('[\r\n][\r\n]+',markdown)
    res = list(filter(lambda x: x,[block.strip() for block in blocks]))    
    return res

def block_to_block_type(block):
    if block.startswith(("#")):
        return "heading"
    elif block.startswith('```') and block.endswith('```'):
        return "code"
    elif block.startswith('>'):
        return "quote"
    elif block.startswith(('* ','- ')):
        return "unordered_list"
    elif block.startswith('1.'):
        return "ordered_list"
    else:
        return "paragraph"


def text_node_to_html_node_v2(text_node):
    node_types = [
        "text",
        "bold",
        "italic",
        "code",
        "link",
        "image",
        "inline_quote",
        "inline_list_item" 
    ]

    if not isinstance(text_node, TextNode):
        raise TypeError("The provided node is not a TextNode")
    if text_node.text_type not in node_types:
        raise TypeError("Text node provided is from incorrect type")

    match text_node.text_type:
        case "text":
            return HTMLNode(None, text_node.text)
        case "bold":
            return HTMLNode("b", text_node.text)
        case "italic":
            return HTMLNode("i", text_node.text)
        case "code":
            return HTMLNode("code", text_node.text)
        case "link":
            return HTMLNode("a", text_node.text, None, {"href": text_node.url})
        case "image":
            return HTMLNode("img", "", None, {"src": text_node.url, "alt": text_node.text})
        case "inline_quote":
            return HTMLNode("q", text_node.text)
        case "inline_list_item":
            return HTMLNode("span", text_node.text, {"class": "list-item"})


def text_to_children(text):
    text_node = TextNode(text,"text")

    # Process for images
    nodes = split_nodes_image([text_node])  
    # Links
    nodes = split_nodes_link(nodes) 
    # Bold
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    # Italic
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    # Code
    nodes = split_nodes_delimiter(nodes, "`", "code")
    
    html_nodes = []
    for node in nodes:
        #print(f"Node type: {node.text_type}, Text: {node.text}")
        html_nodes.append(text_node_to_html_node_v2(node))
    
    return html_nodes

def determine_header_level(text):
    count = 0

    for char in text:
        if char == "#":
            count += 1
        else:
            break

    return count

def strip_list_marker(item):
    return re.sub(r'^(\d+\.|-|\*|\+)\s+', '', item)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    main_Html = HTMLNode('div')

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == 'paragraph':
            node = HTMLNode('p')
            node.children = text_to_children(block)
        elif block_type == 'heading':
            level = determine_header_level(block)
            node = HTMLNode(f"h{level}")
            heading_text = block.lstrip('#').strip()
            node.children = text_to_children(heading_text)
        elif block_type == "code":
            code_content = block.strip().strip('`').strip('\n')
            
            node = HTMLNode("pre")
            code_node = HTMLNode("code")
            code_text_node = HTMLNode(None, code_content)
            
            code_node.add_child(code_text_node)
            node.add_child(code_node)
        elif block_type == "quote":
            node = HTMLNode("blockquote")
            #p_node = HTMLNode("p")
            node.children = text_to_children(block.lstrip("> ").strip())
            #node.add_child(p_node)
        elif block_type == 'unordered_list':
            node = HTMLNode('ul')
            # Handle list items
            #print(f"Processing unordered list: '{block}'")
            for item in block.split("\n"):
                li_node = HTMLNode('li')
                li_node.children = text_to_children(strip_list_marker(item).strip())
                node.add_child(li_node)
        elif block_type == 'ordered_list':
            node = HTMLNode('ol')
            # Handle list items
            for item in block.split("\n"):
                li_node = HTMLNode('li')
                li_node.children = text_to_children(strip_list_marker(item).strip())
                node.add_child(li_node)
        else:
            raise Exception("Uknown block type")
        main_Html.add_child(node) 

    return main_Html

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith(("#","##","###","####","#####","######")):
            return line.lstrip("#").strip()
    raise Exception('No Header!')
    