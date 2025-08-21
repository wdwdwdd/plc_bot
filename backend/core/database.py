from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import yaml
import os


def load_db_config():
    config_path = os.getenv("CONFIG_PATH", "../config/settings.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        cfg = config.get("database", {})
        # Allow environment overrides (useful in docker-compose)
        return {
            "host": os.getenv("DB_HOST", cfg.get("host", "localhost")),
            "port": int(os.getenv("DB_PORT", cfg.get("port", 5432))),
            "name": os.getenv("DB_NAME", cfg.get("name", "plc_monitor")),
            "user": os.getenv("DB_USER", cfg.get("user", "admin")),
            "password": os.getenv("DB_PASSWORD", cfg.get("password", "secret")),
        }


db_config = load_db_config()
DATABASE_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
