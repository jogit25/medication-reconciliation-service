from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone,timedelta
from app.db.database import get_db
from bson import ObjectId

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

    try:
        obj_id = ObjectId(conflict_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid conflict ID")

    result = await db["conflicts"].update_one(
        {"_id": obj_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conflict not found")

    return{
         
    "message": "Conflict resolved",
        "conflict_id": conflict_id
    } 

   
@router.get("/reports/unresolved-conflicts/{clinic}")
async def get_unresolved_conflicts(clinic: str, db=Depends(get_db)):

    pipeline = [
        {
            "$match": {
                "status": "unresolved",
                "sources": clinic
            }
        },
        {
            "$group": {
                "_id": "$patient_id"
            }
        }
    ]

    results = await db["conflicts"].aggregate(pipeline).to_list(length=None)

    return {
        "patients": [r["_id"] for r in results]
    }


@router.get("/reports/high-conflicts")
async def get_high_conflicts(db=Depends(get_db)):

    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

    pipeline = [
        {
            "$match": {
                "created_at": {"$gte": thirty_days_ago}
            }
        },
        {
            "$group": {
                "_id": "$patient_id",
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "count": {"$gte": 2}
            }
        }
    ]

    results = await db["conflicts"].aggregate(pipeline).to_list(length=None)

    return {
    "patients": [
        {"patient_id": r["_id"], "conflict_count": r["count"]}
        for r in results
    ]
}