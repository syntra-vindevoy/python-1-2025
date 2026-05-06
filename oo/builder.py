class Button:
    def __init__(self, text, color, width, height):
        self.text = text
        self.color = color
        self.width = width
        self.height = height

button = Button("Click me", "red", 100, 50)

class ButtonBuilder:
    def __init__(self):
        self.text = None
        self.color = None
        self.width = None
        self.height = None
        self.radius = None

        self.square_corners()

    def set_text(self, text):
        self.text = text

        return self

    def set_color(self, color):
        self.color = color

        return self

    def set_size(self, width, height):
        self.width = width
        self.height = height

        return self

    def rounded_corners(self, radius):
        self.radius = radius
        return self

    def square_corners(self):
        self.radius = None
        return self

    def build(self):
        return Button(self.text, self.color, self.width, self.height)

button = ButtonBuilder().set_text("Click me").set_color("red").build()


# b = ButtonBuilder()
# b.set_text("Click me")
# b.set_color("red").set_size(100, 50)
#
# layout = page(
#     b
# )
#
# def server():
#     def render_b():
#         pass
#
#     b.render = render_b