from typing import List
from app.models.medication import Medication


def normalize_medications(medications: List[Medication]) -> List[dict]:
    seen = set()
    normalized = []

    for med in medications:
        name = med.name.strip().lower()
        dose = med.dose.strip().lower() if med.dose else None
        status = med.status.strip().lower()

        key = (name, dose, status)

        if key not in seen:
            seen.add(key)
            normalized.append({
                "name": name,
                "dose": dose,
                "status": status
            })

    return normalized