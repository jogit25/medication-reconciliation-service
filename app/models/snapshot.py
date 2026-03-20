from pydantic import BaseModel
from typing import List
from enum import Enum
from app.models.medication import Medication


class SourceEnum(str, Enum):
    clinic_emr = "clinic_emr"
    hospital_discharge = "hospital_discharge"
    patient_reported = "patient_reported"


class MedicationSnapshot(BaseModel):
    source: SourceEnum
    medications: List[Medication]