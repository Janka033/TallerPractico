from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.domain.entities.participant import Participant
from src.domain.interfaces.participant_repository import ParticipantRepository
from src.infrastructure.database.models.participant_model import ParticipantModel

def _to_entity(m: ParticipantModel) -> Participant:
    return Participant(id=m.id, name=m.name, email=m.email)

class SQLParticipantRepository(ParticipantRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, email: str) -> Participant:
        m = ParticipantModel(name=name, email=email)
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        return _to_entity(m)

    def get(self, participant_id: int) -> Optional[Participant]:
        m = self.db.get(ParticipantModel, participant_id)
        return _to_entity(m) if m else None

    def get_by_email(self, email: str) -> Optional[Participant]:
        stmt = select(ParticipantModel).where(ParticipantModel.email == email)
        m = self.db.execute(stmt).scalars().first()
        return _to_entity(m) if m else None

    def list(self) -> List[Participant]:
        return [_to_entity(m) for m in self.db.query(ParticipantModel).all()]

    def update(self, participant_id: int, name: str, email: str) -> Optional[Participant]:
        m = self.db.get(ParticipantModel, participant_id)
        if not m:
            return None
        m.name = name
        m.email = email
        self.db.commit()
        self.db.refresh(m)
        return _to_entity(m)

    def delete(self, participant_id: int) -> bool:
        m = self.db.get(ParticipantModel, participant_id)
        if not m:
            return False
        self.db.delete(m)
        self.db.commit()
        return True