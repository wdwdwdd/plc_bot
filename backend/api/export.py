from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import csv
from datetime import datetime
import os

from ..core.database import get_db
from ..models import ProductionData

router = APIRouter(prefix="/export", tags=["export"])


async def create_export_file(
    db: Session, device_id: int, start_time: datetime, end_time: datetime
) -> str:
    data = (
        db.query(ProductionData)
        .filter(
            ProductionData.device_id == device_id,
            ProductionData.timestamp.between(start_time, end_time),
        )
        .all()
    )

    os.makedirs("temp", exist_ok=True)
    filename = f"export_{device_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join("temp", filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["时间戳", "数据点", "数值"])
        for record in data:
            writer.writerow([record.timestamp, record.point_name, record.value])

    return filepath


@router.get("/data/{device_id}")
async def export_data(
    device_id: int,
    start_time: datetime,
    end_time: datetime,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    filepath = await create_export_file(db, device_id, start_time, end_time)
    background_tasks.add_task(os.remove, filepath)
    return FileResponse(filepath, filename=os.path.basename(filepath))
