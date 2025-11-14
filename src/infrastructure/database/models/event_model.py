from sqlalchemy import Column, Integer, String, Text
from src.infrastructure.database.base import Base

class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=False, default=0)