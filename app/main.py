from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from app.parser.parser import write_timetable_to_json
from app.routers import timetable_router

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    trigger = CronTrigger(hour=14, minute=52)
    scheduler.add_job(write_timetable_to_json, trigger)
    scheduler.start()
    
    write_timetable_to_json()
    
    print("Start")
    yield
    print("End")
    scheduler.shutdown()


app = FastAPI(title="Takvim Parser", lifespan=lifespan)

app.include_router(timetable_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Takvim Parser. Created by Q.Muhammad"}
