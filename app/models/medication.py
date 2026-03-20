from pydantic import BaseModel
from typing import Optional


class Medication(BaseModel):
    name: str
    dose: Optional[str] = None
    status: str  

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Medication name cannot be empty")
        return v