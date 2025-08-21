from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class EventResponse(BaseModel):
    id: int
    device_id: int
    level: Literal["info", "warning", "error"]
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True

