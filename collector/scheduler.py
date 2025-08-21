from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from db import save_collected, save_event


class CollectorScheduler:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.scheduler = BackgroundScheduler()
        self.logger = logging.getLogger(__name__)

    def start(self, interval_seconds: int = 5):
        self.scheduler.add_job(
            self._collect_and_save, trigger=IntervalTrigger(seconds=interval_seconds)
        )
        self.scheduler.start()
        self.logger.info("采集调度器已启动")

    def _apply_alarm_rules(self, device_cfg: dict, device_data: dict):
        # 规则格式示例：point 下可定义 alarm: { op: gt/lt/ge/le/eq, threshold: 80, level: warning, message: '温度过高' }
        for point in device_cfg.get("points", []):
            alarm = point.get("alarm")
            if not alarm:
                continue
            name = point.get("name")
            value = device_data.get(name)
            if value is None:
                continue
            op = alarm.get("op", "gt")
            thr = alarm.get("threshold")
            level = alarm.get("level", "warning")
            msg_tpl = alarm.get("message", f"{name} threshold alarm")
            fired = False
            try:
                if op == "gt":
                    fired = value > thr
                elif op == "ge":
                    fired = value >= thr
                elif op == "lt":
                    fired = value < thr
                elif op == "le":
                    fired = value <= thr
                elif op == "eq":
                    fired = value == thr
            except Exception:
                continue
            if fired:
                save_event(
                    device_cfg.get("name"),
                    level,
                    msg_tpl.format(value=value, threshold=thr),
                )

    def _collect_and_save(self):
        try:
            data = self.data_processor.collect_data()
            for device_cfg in self.data_processor.config.get("devices", []):
                name = device_cfg.get("name")
                device_data = data.get(name, {})
                # 保存数据
                save_collected(name, device_data)
                # 应用报警规则
                self._apply_alarm_rules(device_cfg, device_data)
            self.logger.debug(f"采集数据: {data}")
        except Exception as e:
            self.logger.error(f"采集失败: {str(e)}")
