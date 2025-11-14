from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.domain.interfaces.attendance_repository import AttendanceRepository
from src.infrastructure.database.models.attendance_model import AttendanceModel

class SQLAttendanceRepository(AttendanceRepository):
    def __init__(self, db: Session):
        self.db = db

    def is_registered(self, event_id: int, participant_id: int) -> bool:
        stmt = select(AttendanceModel.id).where(
            AttendanceModel.event_id == event_id,
            AttendanceModel.participant_id == participant_id
        )
        return self.db.execute(stmt).first() is not None

    def register(self, event_id: int, participant_id: int) -> None:
        m = AttendanceModel(event_id=event_id, participant_id=participant_id)
        self.db.add(m)
        self.db.commit()

    def count_attendees(self, event_id: int) -> int:
        stmt = select(func.count(AttendanceModel.id)).where(AttendanceModel.event_id == event_id)
        return int(self.db.execute(stmt).scalar() or 0)