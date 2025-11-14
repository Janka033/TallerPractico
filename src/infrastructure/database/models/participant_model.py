from sqlalchemy import Column, Integer, String
from src.infrastructure.database.base import Base

class ParticipantModel(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=False, unique=True)