from fastapi import APIRouter

router = APIRouter()


@router.post("/patients/{patient_id}/medications")
async def ingest_medications(patient_id: str, payload: dict):
    return {
        "message": "Ingestion successful",
        "patient_id": patient_id,
        "data": payload
    }