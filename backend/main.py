import os
import yaml
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .api import data as data_api
from .api import devices as devices_api
from .api import export as export_api
from .api import events as events_api


def setup_logging():
    config_path = os.getenv("CONFIG_PATH", "../config/settings.yaml")
    level = logging.INFO
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logfile = None
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            log_cfg = config.get("logging", {})
            level = getattr(logging, log_cfg.get("level", "INFO"))
            fmt = log_cfg.get("format", fmt)
            logfile = log_cfg.get("file")
    except Exception:
        pass

    logger = logging.getLogger()
    logger.setLevel(level)
    formatter = logging.Formatter(fmt)

    if logfile:
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
        file_handler = RotatingFileHandler(
            logfile, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)


setup_logging()
app = FastAPI(title="PLC Monitor API")


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("uvicorn.access")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} -> {response.status_code}")
    return response


# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers under /api
app.include_router(devices_api.router, prefix="/api")
app.include_router(data_api.router, prefix="/api")
app.include_router(export_api.router, prefix="/api")
app.include_router(events_api.router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
