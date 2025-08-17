from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
import enum

class EventLevel(enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    level = Column(Enum(EventLevel))
    message = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    device = relationship("Device", back_populates="events")
