from dataclasses import dataclass

@dataclass
class Event:
    id: int | None
    name: str
    description: str | None
    capacity: int