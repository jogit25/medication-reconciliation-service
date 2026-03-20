from fastapi import FastAPI
from app.routers import ingest,conflicts



app = FastAPI()

app.include_router(ingest.router)
app.include_router(conflicts.router)



@app.get("/")
async def root():
    return {"message": "Medication Service Running"}