from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.entities.event import Event
from src.domain.interfaces.event_repository import EventRepository
from src.infrastructure.database.models.event_model import EventModel

def _to_entity(m: EventModel) -> Event:
    return Event(id=m.id, name=m.name, description=m.description, capacity=m.capacity)

class SQLEventRepository(EventRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str | None, capacity: int) -> Event:
        m = EventModel(name=name, description=description, capacity=capacity)
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        return _to_entity(m)

    def get(self, event_id: int) -> Optional[Event]:
        m = self.db.get(EventModel, event_id)
        return _to_entity(m) if m else None

    def list(self) -> List[Event]:
        return [_to_entity(m) for m in self.db.query(EventModel).all()]

    def update(self, event_id: int, name: str, description: str | None, capacity: int) -> Optional[Event]:
        m = self.db.get(EventModel, event_id)
        if not m:
            return None
        m.name = name
        m.description = description
        m.capacity = capacity
        self.db.commit()
        self.db.refresh(m)
        return _to_entity(m)

    def delete(self, event_id: int) -> bool:
        m = self.db.get(EventModel, event_id)
        if not m:
            return False
        self.db.delete(m)
        self.db.commit()
        return True