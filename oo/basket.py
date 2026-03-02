from oo.orange import Orange
from oo.apple import Apple

class Basket:
    # PROPERTIES
    location: str = ""
    content: list[Orange | Apple] = []

    # METHODS
    def put_in_basket(self, item: Apple | Orange):
        self.content.append(item)