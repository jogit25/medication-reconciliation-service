from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models.medication import Medication
from app.models.enums import SourceEnum


class MedicationSnapshot(BaseModel):
    source: SourceEnum
    medications: List[Medication]


    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Medication name cannot be empty")
        return v
