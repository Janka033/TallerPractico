from pydantic import BaseModel, Field

class EventCreateDTO(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    capacity: int = Field(ge=0)

class EventUpdateDTO(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    capacity: int = Field(ge=0)

class EventDTO(BaseModel):
    id: int
    name: str
    description: str | None
    capacity: int