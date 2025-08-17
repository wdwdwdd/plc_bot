import yaml
from datetime import datetime
from typing import Dict, Any
from .modbus_client import ModbusClient

class DataProcessor:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.clients: Dict[str, ModbusClient] = {}
        self._init_clients()

    def _load_config(self, path: str) -> dict:
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _init_clients(self):
        for device in self.config['devices']:
            client = ModbusClient(device['ip_address'], device['port'])
            self.clients[device['name']] = client

    def collect_data(self) -> Dict[str, Any]:
        result = {}
        for device in self.config['devices']:
            device_data = {}
            client = self.clients[device['name']]
            if client.connect():
                for point in device['points']:
                    if point['type'] == 'float':
                        value = client.read_float(point['address'])
                    else:
                        value = client.read_holding_registers(point['address'], 1)[0]
                    device_data[point['name']] = value
                client.close()
            result[device['name']] = device_data
        return result
