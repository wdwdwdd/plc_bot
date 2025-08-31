#!/usr/bin/env python3
# plc_relay_scanner.py
# 扫描汇川 Easy522 PLC 的继电器地址和值

import argparse
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

class PLCRelayScanner:
    def __init__(self, host, port=502, unit_id=1):
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.client = None

    def connect(self):
        """连接到PLC"""
        try:
            self.client = ModbusTcpClient(host=self.host, port=self.port, timeout=3)
            return self.client.connect()
        except Exception as e:
            print(f"连接错误: {e}")
            return False

    def disconnect(self):
        """断开连接"""
        if self.client:
            self.client.close()

    def scan_relays(self, start_address, count):
        """
        扫描继电器地址和值
        :param start_address: 起始地址
        :param count: 扫描数量
        :return: 继电器地址和值的字典
        """
        try:
            # 低频批量读取
            response = self.client.read_coils(address=start_address, count=count, device_id=self.unit_id)
            if response.isError():
                print(f"读取错误: {response}")
                return None

            # 提取继电器状态
            relays = {}
            for i in range(count):
                relays[f"Relay_{start_address + i}"] = bool(response.bits[i])
            return relays

        except ModbusException as e:
            print(f"Modbus错误: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description="PLC 继电器扫描工具")
    parser.add_argument("--host", required=True, help="PLC IP地址")
    parser.add_argument("--port", type=int, default=502, help="Modbus端口")
    parser.add_argument("--unit", type=int, default=1, help="Modbus单元ID")
    parser.add_argument("--start", type=int, default=0, help="起始继电器地址")
    parser.add_argument("--count", type=int, default=2, help="扫描继电器数量")

    args = parser.parse_args()

    # 创建扫描器实例
    scanner = PLCRelayScanner(args.host, args.port, args.unit)

    if not scanner.connect():
        print("无法连接到PLC")
        return

    try:
        # 扫描继电器
        relays = scanner.scan_relays(args.start, args.count)
        if relays:
            print("\n继电器状态:")
            for addr, value in relays.items():
                print(f"{addr}: {'ON' if value else 'OFF'}")
        else:
            print("扫描失败")

    finally:
        scanner.disconnect()

if __name__ == "__main__":
    main()