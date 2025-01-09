from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from database.google_calendar import create_google_calendar_event

calendar_router = APIRouter(prefix="/calendar", tags=["Google Calendar"])

class CalendarEvent(BaseModel):
    title: str
    description: str = ""
    start_datetime: str
    end_datetime: str
    attendees: list[str] = []

@calendar_router.post("/create-event")
async def create_event(event: CalendarEvent):
    try:
        start_datetime = datetime.strptime(event.start_datetime, "%Y-%m-%d %H:%M").isoformat() + "-07:00"
        end_datetime = datetime.strptime(event.end_datetime, "%Y-%m-%d %H:%M").isoformat() + "-07:00"
        event_data = event.dict()
        event_data['start_datetime'] = start_datetime
        event_data['end_datetime'] = end_datetime
        event_result = create_google_calendar_event(event_data)
        return {"message": "Событие успешно создано.", "event": event_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
