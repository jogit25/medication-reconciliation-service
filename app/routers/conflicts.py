from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from app.db.database import get_db

router = APIRouter()


@router.put("/conflicts/{conflict_id}/resolve")
async def resolve_conflict(
    conflict_id: str,
    payload: dict,
    db=Depends(get_db)
):
    update_data = {
        "status": "resolved",
        "resolution_reason": payload.get("reason"),
        "resolved_by": payload.get("resolved_by"),
        "resolved_at": datetime.now(timezone.utc)
    }

    await db["conflicts"].update_one(
        {"_id": conflict_id},
        {"$set": update_data}
    )

    return {
        "message": "Conflict resolved",
        "conflict_id": conflict_id
    }