from abc import ABC, abstractmethod


class ShinyView(ABC):
    @abstractmethod
    def __call__(self):
        pass
