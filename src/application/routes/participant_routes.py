from typing import List, TYPE_CHECKING
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.dtos.participant_dto import ParticipantCreateDTO, ParticipantUpdateDTO, ParticipantDTO
from src.api.deps import get_participant_controller

if TYPE_CHECKING:
    from src.application.controllers.participant_controller import ParticipantController

router = APIRouter(prefix="/participants", tags=["participants"])

@router.post("", response_model=ParticipantDTO, status_code=status.HTTP_201_CREATED)
def create_participant(payload: ParticipantCreateDTO, controller = Depends(get_participant_controller)):
    try:
        return controller.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[ParticipantDTO])
def list_participants(controller = Depends(get_participant_controller)):
    return controller.list()

@router.get("/{participant_id}", response_model=ParticipantDTO)
def get_participant(participant_id: int, controller = Depends(get_participant_controller)):
    try:
        return controller.get(participant_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{participant_id}", response_model=ParticipantDTO)
def update_participant(participant_id: int, payload: ParticipantUpdateDTO, controller = Depends(get_participant_controller)):
    try:
        return controller.update(participant_id, payload.name, payload.email)
    except ValueError as e:
        msg = str(e)
        code = 400 if "Email" in msg else 404
        raise HTTPException(status_code=code, detail=msg)

@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant(participant_id: int, controller = Depends(get_participant_controller)):
    try:
        controller.delete(participant_id)
        return
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))