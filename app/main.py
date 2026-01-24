from contextlib import asynccontextmanager
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI

from app.parser.parser import write_timetable_to_json
from app.routers import timetable_router

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    trigger = IntervalTrigger(hours=1, start_date=datetime.now())
    write_timetable_to_json()
    scheduler.add_job(write_timetable_to_json, trigger)
    scheduler.start()

    print("Start")
    yield
    print("End")
    scheduler.shutdown()


app = FastAPI(title="Takvim Parser", lifespan=lifespan)

app.include_router(timetable_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Takvim Parser. Created by Q.Muhammad"}
