from typing import List, Optional
from src.domain.entities.event import Event
from src.domain.interfaces.event_repository import EventRepository

class EventService:
    def __init__(self, repo: EventRepository):
        self.repo = repo

    def create(self, name: str, description: str | None, capacity: int) -> Event:
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")
        return self.repo.create(name, description, capacity)

    def get(self, event_id: int) -> Optional[Event]:
        return self.repo.get(event_id)

    def list(self) -> List[Event]:
        return self.repo.list()

    def update(self, event_id: int, name: str, description: str | None, capacity: int) -> Optional[Event]:
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")
        return self.repo.update(event_id, name, description, capacity)

    def delete(self, event_id: int) -> bool:
        return self.repo.delete(event_id)