from dataclasses import dataclass

@dataclass
class Participant:
    id: int | None
    name: str
    email: str