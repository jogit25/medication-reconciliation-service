from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models.medication import Medication
from app.models.enums import SourceEnum


class MedicationSnapshot(BaseModel):
    source: SourceEnum
    medications: List[Medication]
