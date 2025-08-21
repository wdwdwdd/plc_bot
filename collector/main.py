import logging
import os
import yaml
from data_processor import DataProcessor
from scheduler import CollectorScheduler


def setup_logging():
    # default
    level = logging.INFO
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    try:
        config_path = os.getenv("CONFIG_PATH", "../config/settings.yaml")
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)
            log_cfg = (cfg or {}).get("logging", {})
            level = getattr(logging, log_cfg.get("level", "INFO"))
            fmt = log_cfg.get("format", fmt)
    except Exception:
        pass
    logging.basicConfig(level=level, format=fmt)


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    devices_path = os.getenv(
        "DEVICES_CONFIG_PATH", os.getenv("CONFIG_PATH", "../config/devices.yaml")
    )
    # Interval can be overridden by settings.yaml collector.interval
    interval = int(os.getenv("COLLECT_INTERVAL", "0") or 0)
    try:
        with open(os.getenv("CONFIG_PATH", "../config/settings.yaml"), "r") as f:
            cfg = yaml.safe_load(f) or {}
            interval = interval or int(
                (cfg.get("collector", {}) or {}).get("interval", 5)
            )
    except Exception:
        interval = interval or 5

    processor = DataProcessor(devices_path)
    scheduler = CollectorScheduler(processor)

    try:
        scheduler.start(interval)
        logger.info("PLC数据采集服务已启动")
        # 保持程序运行
        import time

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("服务停止")


if __name__ == "__main__":
    main()
