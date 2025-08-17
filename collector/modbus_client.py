import asyncio
from pymodbus.client import AsyncModbusTcpClient
from typing import Dict, Any
import logging

class ModbusClient:
    def __init__(self, host: str, port: int = 502):
        self.client = AsyncModbusTcpClient(host, port)
        self.logger = logging.getLogger(__name__)

    async def connect(self) -> bool:
        try:
            await self.client.connect()
            return True
        except Exception as e:
            self.logger.error(f"连接失败: {str(e)}")
            return False

    async def read_holding_registers(self, address: int, count: int) -> list:
        try:
            result = await self.client.read_holding_registers(address, count)
            return result.registers if result else []
        except Exception as e:
            self.logger.error(f"读取寄存器失败: {str(e)}")
            return []

    async def write_holding_register(self, address: int, value: int) -> bool:
        try:
            result = await self.client.write_register(address, value)
            return result.isError() == False
        except Exception as e:
            self.logger.error(f"写入寄存器失败: {str(e)}")
            return False

    async def read_float(self, address: int) -> float:
        """读取浮点数值（占用2个寄存器）"""
        registers = await self.read_holding_registers(address, 2)
        if len(registers) == 2:
            import struct
            combined = (registers[0] << 16) + registers[1]
            return struct.unpack('f', struct.pack('I', combined))[0]
        return 0.0

    async def close(self):
        await self.client.close()
