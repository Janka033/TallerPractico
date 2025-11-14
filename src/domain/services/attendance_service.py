from typing import Dict
from src.domain.interfaces.attendance_repository import AttendanceRepository
from src.domain.interfaces.event_repository import EventRepository
from src.domain.interfaces.participant_repository import ParticipantRepository
from src.infrastructure.cache.cache_client import CacheClient

class AttendanceService:
    def __init__(self, attendance_repo: AttendanceRepository, event_repo: EventRepository,
                 participant_repo: ParticipantRepository, cache: CacheClient):
        self.attendance_repo = attendance_repo
        self.event_repo = event_repo
        self.participant_repo = participant_repo
        self.cache = cache

    def register(self, event_id: int, participant_id: int) -> Dict[str, str]:
        event = self.event_repo.get(event_id)
        if not event:
            raise ValueError("Event not found")
        participant = self.participant_repo.get(participant_id)
        if not participant:
            raise ValueError("Participant not found")
        if self.attendance_repo.is_registered(event_id, participant_id):
            raise ValueError("Participant already registered for this event")

        current = self.attendance_repo.count_attendees(event_id)
        if current >= event.capacity:
            raise ValueError("Event is at full capacity")

        self.attendance_repo.register(event_id, participant_id)
        # invalidar/actualizar caché
        cache_key = f"event:{event_id}:registrations"
        self.cache.delete(cache_key)
        return {"status": "registered"}

    def event_stats(self, event_id: int) -> Dict[str, float | int]:
        event = self.event_repo.get(event_id)
        if not event:
            raise ValueError("Event not found")
        cache_key = f"event:{event_id}:registrations"
        cached = self.cache.get(cache_key)
        if cached is not None:
            registered = int(cached)
        else:
            registered = self.attendance_repo.count_attendees(event_id)
            self.cache.set(cache_key, str(registered))
        available = max(event.capacity - registered, 0)
        percent = (registered / event.capacity * 100.0) if event.capacity > 0 else 0.0
        return {
            "event_id": event_id,
            "capacity": event.capacity,
            "registered": registered,
            "available": available,
            "occupancy_percent": round(percent, 2),
        }