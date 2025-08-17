import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.base import Base
from backend.core.database import engine
from backend.models import Device, User, ProductionData, Event
from backend.core.security import get_password_hash

def init_database():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建管理员账户
    from sqlalchemy.orm import Session
    with Session(engine) as session:
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        session.add(admin)
        session.commit()

if __name__ == "__main__":
    init_database()
    print("数据库初始化完成！")
