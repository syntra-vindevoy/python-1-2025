from abc import ABC, abstractmethod
from typing import Any

from shiny_app.core.utils import enable_logging


@enable_logging
class ShinyAppController(ABC):
    @abstractmethod
    def __call__(self, inputs: Any, outputs: Any, session: Any) -> None: ...
