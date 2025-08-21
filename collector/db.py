import os
import yaml
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


def _load_db_url() -> str:
    config_path = os.getenv("CONFIG_PATH", "../config/settings.yaml")
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f) or {}
    db = cfg.get("database", {})
    host = os.getenv("DB_HOST", db.get("host", "localhost"))
    port = os.getenv("DB_PORT", db.get("port", 5432))
    name = os.getenv("DB_NAME", db.get("name", "plc_monitor"))
    user = os.getenv("DB_USER", db.get("user", "admin"))
    password = os.getenv("DB_PASSWORD", db.get("password", "secret"))
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(_load_db_url(), pool_pre_ping=True)
    return _engine


def _get_device_id(session: Session, device_name: str):
    res = session.execute(
        text("SELECT id FROM devices WHERE name = :name"), {"name": device_name}
    ).first()
    return res[0] if res else None


def save_collected(device_name: str, data: dict):
    engine = get_engine()
    with Session(engine) as session:
        device_id = _get_device_id(session, device_name)
        if not device_id:
            return
        for point_name, value in data.items():
            session.execute(
                text(
                    """
                    INSERT INTO production_data (device_id, point_name, value, timestamp)
                    VALUES (:device_id, :point_name, :value, NOW())
                    """
                ),
                {
                    "device_id": device_id,
                    "point_name": point_name,
                    "value": float(value),
                },
            )
        session.commit()


def save_event(device_name: str, level: str, message: str):
    engine = get_engine()
    with Session(engine) as session:
        device_id = _get_device_id(session, device_name)
        if not device_id:
            return
        session.execute(
            text(
                """
                INSERT INTO events (device_id, level, message, timestamp)
                VALUES (:device_id, :level, :message, NOW())
                """
            ),
            {"device_id": device_id, "level": level, "message": message},
        )
        session.commit()
