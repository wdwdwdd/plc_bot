import logging
from data_processor import DataProcessor
from scheduler import CollectorScheduler
import os

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    config_path = os.getenv('CONFIG_PATH', '../config/devices.yaml')
    interval = int(os.getenv('COLLECT_INTERVAL', '5'))
    
    processor = DataProcessor(config_path)
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
