from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging

class CollectorScheduler:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.scheduler = BackgroundScheduler()
        self.logger = logging.getLogger(__name__)

    def start(self, interval_seconds: int = 5):
        self.scheduler.add_job(
            self._collect_and_save,
            trigger=IntervalTrigger(seconds=interval_seconds)
        )
        self.scheduler.start()
        self.logger.info("采集调度器已启动")

    def _collect_and_save(self):
        try:
            data = self.data_processor.collect_data()
            # TODO: 将数据保存到数据库
            self.logger.debug(f"采集数据: {data}")
        except Exception as e:
            self.logger.error(f"采集失败: {str(e)}")
