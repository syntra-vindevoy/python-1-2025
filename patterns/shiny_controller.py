from abc import ABC, abstractmethod


class ShinyController(ABC):
    @abstractmethod
    def __call__(self, inputs, outputs, session):
        pass
