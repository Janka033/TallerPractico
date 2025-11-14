from typing import List
from src.domain.services.event_service import EventService
from src.application.dtos.event_dto import EventCreateDTO, EventUpdateDTO, EventDTO

class EventController:
    def __init__(self, service: EventService):
        self.service = service

    def create(self, payload: EventCreateDTO) -> EventDTO:
        e = self.service.create(payload.name, payload.description, payload.capacity)
        return EventDTO(id=e.id or 0, name=e.name, description=e.description, capacity=e.capacity)

    def list(self) -> List[EventDTO]:
        return [EventDTO(id=e.id or 0, name=e.name, description=e.description, capacity=e.capacity) for e in self.service.list()]

    def get(self, event_id: int) -> EventDTO:
        e = self.service.get(event_id)
        if not e:
            raise ValueError("Event not found")
        return EventDTO(id=e.id or 0, name=e.name, description=e.description, capacity=e.capacity)

    def update(self, event_id: int, payload: EventUpdateDTO) -> EventDTO:
        e = self.service.update(event_id, payload.name, payload.description, payload.capacity)
        if not e:
            raise ValueError("Event not found")
        return EventDTO(id=e.id or 0, name=e.name, description=e.description, capacity=e.capacity)

    def delete(self, event_id: int) -> None:
        ok = self.service.delete(event_id)
        if not ok:
            raise ValueError("Event not found")