import html

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        html = ""
        if self.tag:
            html += f"<{self.tag}"
            html += self.props_to_html()  # Use the props_to_html method here
            html += ">"
        
        if self.children:
            for child in self.children:
                if isinstance(child, HTMLNode):
                    html += child.to_html()
                elif isinstance(child, str):
                    html += child
                else:
                    raise ValueError(f"Invalid child type: {type(child)}")
        
        if self.value:
            html += self.value
        
        if self.tag:
            html += f"</{self.tag}>"
        return html
        
    def props_to_html(self):
        if not self.props:
            return ""
        return ''.join(f' {key}="{value}"' for key, value in self.props.items())
    
    def add_child(self, child):
        if self.children is None:
            self.children = []
        self.children.append(child)

    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}\n, {self.value}\n, {self.children}\n, {self.props}\n'
    

class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None):
       super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("leafnode must have a value")
        if self.tag is None:
            return str(self.value)
        
        #print(f'Debug: LeafNode with tag "{self.tag}" and value "{self.value}"')
        escaped_value = html.escape(self.value)
        match self.tag:
            case "p":
                return f'<{self.tag}>{escaped_value}</{self.tag}>'
            case "a":
                return f'<a{self.props_to_html()}>{escaped_value}</a>'
        return f'<{self.tag}>{escaped_value}</{self.tag}>'
            
    def __eq__(self, other) -> bool:
        return (
            self.value == other.value and
            self.tag == other.tag and
            self.props == other.props
        )
    
    def __repr__(self) -> str:
        return f'LeafNode(value={self.value}, tag={self.tag}, props={self.props})'

class ParentNode(HTMLNode):
    def __init__(self, tag, children,  props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag needs to be specified")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Children needs to be specified")
        
        child_res = ""
        for child in self.children:
            child_html = child.to_html()
            if child_html is None:
                raise ValueError("Encountered a child with no valid HTML content")
            #print(f'Debug: child.to_html() returned {child_html}')  # Debug print
            child_res += str(child_html)

        return f'<{self.tag}>{child_res}</{self.tag}>'