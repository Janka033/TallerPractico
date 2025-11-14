from typing import List
from src.domain.services.participant_service import ParticipantService
from src.application.dtos.participant_dto import (
    ParticipantCreateDTO, ParticipantUpdateDTO, ParticipantDTO
)

class ParticipantController:
    def __init__(self, service: ParticipantService):
        self.service = service

    def create(self, payload: ParticipantCreateDTO) -> ParticipantDTO:
        p = self.service.create(payload.name, payload.email)
        return ParticipantDTO(id=p.id or 0, name=p.name, email=p.email)

    def list(self) -> List[ParticipantDTO]:
        return [ParticipantDTO(id=p.id or 0, name=p.name, email=p.email) for p in self.service.list()]

    def get(self, participant_id: int) -> ParticipantDTO:
        p = self.service.get(participant_id)
        if not p:
            raise ValueError("Participant not found")
        return ParticipantDTO(id=p.id or 0, name=p.name, email=p.email)

    def update(self, participant_id: int, payload: ParticipantUpdateDTO) -> ParticipantDTO:
        p = self.service.update(participant_id, payload.name, payload.email)
        if not p:
            raise ValueError("Participant not found")
        return ParticipantDTO(id=p.id or 0, name=p.name, email=p.email)

    def delete(self, participant_id: int) -> None:
        ok = self.service.delete(participant_id)
        if not ok:
            raise ValueError("Participant not found")