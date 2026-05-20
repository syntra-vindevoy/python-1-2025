from dataclasses import dataclass

from energy.models.base_table import BaseTable


@dataclass(slots=True)
class ScheduleEntry:
    rec_id: int
    device_id: int
    start: str
    end: str
    moveable: bool = False


class Schedule(BaseTable):
    _FILE = "schedule.yaml"
    _MODEL = ScheduleEntry
