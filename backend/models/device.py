from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    ip_address = Column(String(15), nullable=False)
    port = Column(Integer, default=502)
    is_active = Column(Boolean, default=True)
    description = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    data_points = relationship("DataPoint", back_populates="device")
