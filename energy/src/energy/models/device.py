from abc import ABC
from dataclasses import dataclass


@dataclass(slots=True)
class Device(ABC):
    pass
