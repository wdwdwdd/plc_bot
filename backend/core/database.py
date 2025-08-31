import redis
import os

def load_db_config():
    config_path = os.getenv("CONFIG_PATH", "../config/settings.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        cfg = config.get("redis", {})
        # Allow environment overrides
        return {
            "host": os.getenv("REDIS_HOST", cfg.get("host", "localhost")),
            "port": int(os.getenv("REDIS_PORT", cfg.get("port", 6379))),
            "db": int(os.getenv("REDIS_DB", cfg.get("db", 0))),
        }

redis_client = redis.Redis(**load_db_config())


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
