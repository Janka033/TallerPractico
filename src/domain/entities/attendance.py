from dataclasses import dataclass

@dataclass
class Attendance:
    id: int | None
    event_id: int
    participant_id: int