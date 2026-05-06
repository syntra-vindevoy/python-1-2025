from hello_controller import HelloController
from hello_model import HelloModel
from hello_view import HelloView
from shiny_application import ShinyApplication


class HelloApplication(ShinyApplication):
    def __init__(self):
        super().__init__(HelloModel, HelloView, HelloController)
