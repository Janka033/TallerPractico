from typing import Dict
from src.domain.services.attendance_service import AttendanceService
from src.application.dtos.attendance_dto import RegisterAttendanceDTO

class AttendanceController:
    def __init__(self, service: AttendanceService):
        self.service = service

    def register(self, payload: RegisterAttendanceDTO) -> Dict[str, str]:
        return self.service.register(payload.event_id, payload.participant_id)

    def stats(self, event_id: int):
        return self.service.event_stats(event_id)