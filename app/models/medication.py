from pydantic import BaseModel
from typing import Optional


class Medication(BaseModel):
    name: str
    dose: Optional[str] = None
    status: str  