from typing import List, Optional
from src.domain.entities.participant import Participant
from src.domain.interfaces.participant_repository import ParticipantRepository

class ParticipantService:
    def __init__(self, repo: ParticipantRepository):
        self.repo = repo

    def create(self, name: str, email: str) -> Participant:
        existing = self.repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        return self.repo.create(name, email)

    def get(self, participant_id: int) -> Optional[Participant]:
        return self.repo.get(participant_id)

    def list(self) -> List[Participant]:
        return self.repo.list()

    def update(self, participant_id: int, name: str, email: str) -> Optional[Participant]:
        other = self.repo.get_by_email(email)
        if other and other.id != participant_id:
            raise ValueError("Email already registered by another participant")
        return self.repo.update(participant_id, name, email)

    def delete(self, participant_id: int) -> bool:
        return self.repo.delete(participant_id)