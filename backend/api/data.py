from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ..models import ProductionData
from ..schemas.production import ProductionDataResponse
from ..core.database import get_db

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/recent/{device_id}", response_model=List[ProductionDataResponse])
def get_recent_data(
    device_id: int,
    hours: Optional[int] = Query(24, ge=1, le=168),
    point_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProductionData).filter(
        ProductionData.device_id == device_id,
        ProductionData.timestamp >= datetime.utcnow() - timedelta(hours=hours)
    )
    
    if point_name:
        query = query.filter(ProductionData.point_name == point_name)
        
    return query.order_by(ProductionData.timestamp.desc()).all()

@router.get("/statistics/{device_id}")
def get_statistics(
    device_id: int,
    point_name: str,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db)
):
    data = db.query(ProductionData).filter(
        ProductionData.device_id == device_id,
        ProductionData.point_name == point_name,
        ProductionData.timestamp.between(start_time, end_time)
    ).all()
    
    if not data:
        return {"message": "No data found"}
        
    values = [d.value for d in data]
    return {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
        "count": len(values)
    }
