from fastapi import APIRouter, Depends
from datetime import datetime,timezone
from app.db.database import get_db
from app.models.snapshot import MedicationSnapshot
from app.services.normalization import normalize_medications
from app.services.conflict_detection import detect_conflicts

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

    previous = await db["medication_snapshots"].find_one(
        {"patient_id": patient_id},
        sort=[("timestamp", -1)]
    )

    old_meds = previous["medications"] if previous else []

    conflicts = detect_conflicts(data["medications"], old_meds)
  
    for conflict in conflicts:
        conflict_doc = {
            "patient_id": patient_id,
            "type": conflict["type"],
            "medications": conflict["medications"],
            "sources": [snapshot.source],
            "status": "unresolved",
            "created_at": datetime.now(timezone.utc)
        }

    await db["conflicts"].insert_one(conflict_doc)

    


    await db["medication_snapshots"].insert_one(data)

    return {
        "message": "Snapshot stored successfully",
        "patient_id": patient_id
    }