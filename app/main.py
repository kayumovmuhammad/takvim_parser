from fastapi import FastAPI
from app.routers import timetable_router

app = FastAPI(title="Takvim Parser")

app.include_router(timetable_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Takvim Parser. Created by Q.Muhammad"}
