from abc import ABC, abstractmethod
from typing import Any

import uvicorn
from shiny import App

from logfac import LoggingObject


class ShinyApplication(ABC, LoggingObject):
    @property
    @abstractmethod
    def layout(self): ...

    @classmethod
    @abstractmethod
    def serve(cls, inputs: Any, outputs: Any, session: Any) -> None: ...

    def __init__(self):
        self.logger.trace(f"entering {__class__.__name__}.__init__")

        super().__init__()
        self.app = App(self.layout, self.serve)

        self.logger.trace(f"exiting {__class__.__name__}.__init__")

    async def __call__(self, scope, receive, send):
        self.logger.trace(f"entering {__class__.__name__}.__call__")
        await self.app(scope, receive, send)
        self.logger.trace(f"exiting {__class__.__name__}.__call__")

    def run(self, **kwargs):
        self.logger.trace(f"entering run with kwargs={kwargs}")
        self.logger.success("starting server")

        uvicorn.run(self.app, **kwargs)

        self.logger.critical("stopping server")
