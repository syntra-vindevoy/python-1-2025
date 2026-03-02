from oo.apple import Apple
from oo.orange import Orange


class Basket:
    location: str = ""
    content: list[Orange | Apple] = []

    def put_in_basket(self, item: Orange | Apple):
        self.content.append(item)