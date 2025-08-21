from pydantic import BaseModel
from typing import Optional


class DeviceBase(BaseModel):
    name: str
    ip_address: str
    port: int = 502
    description: Optional[str] = None
    is_active: bool = True


class DeviceCreate(DeviceBase):
    pass


class DeviceResponse(DeviceBase):
    id: int

    class Config:
        orm_mode = True

