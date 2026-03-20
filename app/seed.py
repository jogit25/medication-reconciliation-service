import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "your_uri_here"


async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["medication_db"]

    data = {
        "patient_id": "seed_1",
        "source": "clinic_emr",
        "medications": [
            {"name": "drugA", "dose": "10mg", "status": "active"}
        ],
        "timestamp": datetime.now(timezone.utc)
    }

    await db["medication_snapshots"].insert_one(data)
    print("Seed inserted")


asyncio.run(seed())