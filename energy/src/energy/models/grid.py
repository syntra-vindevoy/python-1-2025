from dataclasses import dataclass


@dataclass(slots=True)
class Grid:
    name: str

    def deliver_energy(self):
        pass

    def absorb_energy(self):
        pass
