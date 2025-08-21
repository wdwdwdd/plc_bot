from pydantic import BaseModel
from datetime import datetime


class ProductionDataResponse(BaseModel):
    id: int
    device_id: int
    point_name: str
    value: float
    timestamp: datetime

    class Config:
        orm_mode = True

