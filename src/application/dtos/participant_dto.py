from pydantic import BaseModel, Field, EmailStr

class ParticipantCreateDTO(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr

class ParticipantUpdateDTO(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr

class ParticipantDTO(BaseModel):
    id: int
    name: str
    email: EmailStr