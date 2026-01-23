import json
from fastapi import APIRouter

router = APIRouter(prefix="/timetable", tags=["Timetable"])


@router.get("/read")
async def get_timetable():
    with open("parser/data.json", "r") as file:
        data = file.read()
        data_json = json.loads(data)
    
    return data_json
