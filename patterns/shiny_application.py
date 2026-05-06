from shiny import App


class ShinyApplication:
    def __init__(self, model_cls, view_cls, controller_cls):
        self.model = model_cls()
        self.view = view_cls()
        self.controller = controller_cls()

    def run(self):
        app = App(self.view(), self.controller)

        app.run()
