import json

from fastapi import APIRouter

from app.parser.parser import write_timetable_to_json

router = APIRouter(prefix="/timetable", tags=["Timetable"])


@router.get("/read")
async def get_timetable():
    with open("./app/parser/data.json", "r") as file:
        data = file.read()
        data_json = json.loads(data)

    return data_json
