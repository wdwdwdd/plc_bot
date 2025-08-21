from pymodbus.client.sync import ModbusTcpClient
import logging
import struct


class ModbusClient:
    def __init__(self, host: str, port: int = 502):
        self.host = host
        self.port = port
        self.client = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        try:
            self.client = ModbusTcpClient(self.host, port=self.port)
            return self.client.connect()
        except Exception as e:
            self.logger.error(f"连接失败: {str(e)}")
            return False

    def read_holding_registers(self, address: int, count: int) -> list:
        try:
            if not self.client:
                return []
            result = self.client.read_holding_registers(address, count)
            return result.registers if result else []
        except Exception as e:
            self.logger.error(f"读取寄存器失败: {str(e)}")
            return []

    def write_holding_register(self, address: int, value: int) -> bool:
        try:
            if not self.client:
                return False
            result = self.client.write_register(address, value)
            return not result.isError()
        except Exception as e:
            self.logger.error(f"写入寄存器失败: {str(e)}")
            return False

    def read_float(self, address: int) -> float:
        """读取浮点数值（占用2个寄存器）"""
        registers = self.read_holding_registers(address, 2)
        if len(registers) == 2:
            combined = (registers[0] << 16) + registers[1]
            return struct.unpack("f", struct.pack("I", combined))[0]
        return 0.0

    def close(self):
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
            finally:
                self.client = None
