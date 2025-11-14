from typing import List, TYPE_CHECKING
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.dtos.event_dto import EventCreateDTO, EventUpdateDTO, EventDTO
from src.api.deps import get_event_controller

if TYPE_CHECKING:
    from src.application.controllers.event_controller import EventController

router = APIRouter(prefix="/events", tags=["events"])

@router.post("", response_model=EventDTO, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreateDTO, controller = Depends(get_event_controller)):
    try:
        return controller.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[EventDTO])
def list_events(controller = Depends(get_event_controller)):
    return controller.list()

@router.get("/{event_id}", response_model=EventDTO)
def get_event(event_id: int, controller = Depends(get_event_controller)):
    try:
        return controller.get(event_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{event_id}", response_model=EventDTO)
def update_event(event_id: int, payload: EventUpdateDTO, controller = Depends(get_event_controller)):
    try:
        return controller.update(event_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, controller = Depends(get_event_controller)):
    try:
        controller.delete(event_id)
        return
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))