from pydantic import BaseModel, Field

class RegisterAttendanceDTO(BaseModel):
    event_id: int = Field(ge=1)
    participant_id: int = Field(ge=1)