class TextNode:
    def  __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, object) -> bool:
        return True if (object.text == self.text and 
                        object.text_type == self.text_type and 
                        object.url == self.url) else False
        
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"