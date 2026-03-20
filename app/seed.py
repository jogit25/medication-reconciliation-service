import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["medication_db"]

    for i in range(1, 11):
        await db["medication_snapshots"].insert_one({
            "patient_id": f"patient_{i}",
            "source": "clinic_emr",
            "medications": [
                {"name": "druga", "dose": "10mg", "status": "active"}
            ],
            "timestamp": datetime.now(timezone.utc)
        })

        await db["medication_snapshots"].insert_one({
            "patient_id": f"patient_{i}",
            "source": "hospital_discharge",
            "medications": [
                {"name": "druga", "dose": "20mg", "status": "active"}
            ],
            "timestamp": datetime.now(timezone.utc)
        })

    print("Seed data inserted")


asyncio.run(seed())