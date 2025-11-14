from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, HTTPException
from src.application.dtos.attendance_dto import RegisterAttendanceDTO
from src.api.deps import get_attendance_controller

if TYPE_CHECKING:
    from src.application.controllers.attendance_controller import AttendanceController

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/register")
def register(payload: RegisterAttendanceDTO, controller = Depends(get_attendance_controller)):
    try:
        return controller.register(payload)
    except ValueError as e:
        msg = str(e)
        code = 404 if "not found" in msg.lower() else 400
        raise HTTPException(status_code=code, detail=msg)

@router.get("/events/{event_id}/stats")
def event_stats(event_id: int, controller = Depends(get_attendance_controller)):
    try:
        return controller.stats(event_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))