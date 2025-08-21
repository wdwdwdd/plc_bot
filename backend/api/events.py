from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..models import Event
from ..schemas.event import EventResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=List[EventResponse])
def list_events(
    skip: int = 0,
    limit: int = Query(100, ge=1, le=1000),
    level: Optional[str] = Query(None, regex="^(info|warning|error)$"),
    device_id: Optional[int] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Event)
    if level:
        q = q.filter(Event.level == level)
    if device_id:
        q = q.filter(Event.device_id == device_id)
    if start_time:
        q = q.filter(Event.timestamp >= start_time)
    if end_time:
        q = q.filter(Event.timestamp <= end_time)
    return q.order_by(Event.timestamp.desc()).offset(skip).limit(limit).all()
