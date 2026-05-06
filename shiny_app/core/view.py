from abc import ABC, abstractmethod

from shiny_app.core.utils import enable_logging


@enable_logging
class ShinyAppView(ABC):
    @abstractmethod
    def __call__(self): ...
