from abc import ABC, abstractmethod

from shiny import App


class ShinyApplication(ABC):
    @abstractmethod
    def layout(self):
        pass

    @abstractmethod
    def server(self, inputs, outputs, session):
        pass

    def run(self):
        app = App(self.layout(), self.server)

        app.run()
