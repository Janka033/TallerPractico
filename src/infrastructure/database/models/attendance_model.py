from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from src.infrastructure.database.base import Base

class AttendanceModel(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("event_id", "participant_id", name="uq_event_participant"),
    )