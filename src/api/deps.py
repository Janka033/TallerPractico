from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.base import get_session_factory
from src.infrastructure.repositories.event_repository_impl import SQLEventRepository
from src.infrastructure.repositories.participant_repository_impl import SQLParticipantRepository
from src.infrastructure.repositories.attendance_repository_impl import SQLAttendanceRepository

from src.domain.services.event_service import EventService
from src.domain.services.participant_service import ParticipantService
from src.domain.services.attendance_service import AttendanceService

from src.infrastructure.cache.cache_client import CacheClient

from src.application.controllers.event_controller import EventController
from src.application.controllers.participant_controller import ParticipantController
from src.application.controllers.attendance_controller import AttendanceController


def get_db() -> Generator[Session, None, None]:
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cache() -> CacheClient:
    return CacheClient()


def get_event_service(db: Session = Depends(get_db)) -> EventService:
    return EventService(SQLEventRepository(db))


def get_participant_service(db: Session = Depends(get_db)) -> ParticipantService:
    return ParticipantService(SQLParticipantRepository(db))


def get_attendance_service(
    db: Session = Depends(get_db),
    cache: CacheClient = Depends(get_cache),
) -> AttendanceService:
    return AttendanceService(
        SQLAttendanceRepository(db),
        SQLEventRepository(db),
        SQLParticipantRepository(db),
        cache,
    )


def get_event_controller(service: EventService = Depends(get_event_service)) -> EventController:
    return EventController(service)


def get_participant_controller(service: ParticipantService = Depends(get_participant_service)) -> ParticipantController:
    return ParticipantController(service)


def get_attendance_controller(service: AttendanceService = Depends(get_attendance_service)) -> AttendanceController:
    return AttendanceController(service)