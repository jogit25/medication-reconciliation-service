from fastapi import APIRouter, Depends
from datetime import datetime,timezone
from app.db.database import get_db
from app.models.snapshot import MedicationSnapshot
from app.services.normalization import normalize_medications

router = APIRouter()


@router.post("/patients/{patient_id}/medications")
async def ingest_medications(
    patient_id: str,
    snapshot: MedicationSnapshot,
    db=Depends(get_db)
):
    data = snapshot.model_dump()
    data["patient_id"] = patient_id
    data["timestamp"] = datetime.now(timezone.utc)
    data["medications"] = normalize_medications(snapshot.medications)


    await db["medication_snapshots"].insert_one(data)

    return {
        "message": "Snapshot stored successfully",
        "patient_id": patient_id
    }