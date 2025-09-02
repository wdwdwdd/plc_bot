#!/usr/bin/env python3
# test_plc_read.py

import argparse
import sys

try:
    from pymodbus.client import ModbusTcpClient, ModbusSerialClient
except ImportError:
    try:
        from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient
    except ImportError:
        print("无法导入 pymodbus 客户端")
        sys.exit(1)

from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse

def read_modbus_tcp(host, port, unit, addr, count=1, reg_type='holding', timeout=3):
    """读取TCP Modbus设备"""
    try:
        client = ModbusTcpClient(host=host, port=port, timeout=timeout)
        
        connection = client.connect()
        if not connection:
            print("TCP连接失败")
            return None
        
        # 根据寄存器类型选择读取方法
        if reg_type == 'coil':
            rr = client.read_coils(address=addr, count=count, device_id=unit)
        elif reg_type == 'discrete':
            rr = client.read_discrete_inputs(address=addr, count=count, device_id=unit)
        elif reg_type == 'input':
            rr = client.read_input_registers(address=addr, count=count, device_id=unit)
        else:  # holding
            rr = client.read_holding_registers(address=addr, count=count, device_id=unit)
        
        client.close()
        
        if rr is None:
            return None
            
        if isinstance(rr, ExceptionResponse):
            print(f"Modbus异常响应: {rr}")
            return None
            
        return rr
    except ModbusException as e:
        print(f"Modbus通信错误: {e}")
        return None
    except Exception as e:
        print(f"其他错误: {e}")
        return None

def read_modbus_rtu(serial_port, baud, parity, stopbits, unit, addr, count=1, reg_type='holding', timeout=3):
    """读取RTU Modbus设备"""
    try:
        client = ModbusSerialClient(
            method='rtu', 
            port=serial_port, 
            baudrate=baud,
            parity=parity, 
            stopbits=stopbits, 
            timeout=timeout
        )
        
        connection = client.connect()
        if not connection:
            print("RTU连接失败")
            return None
        
        # 根据寄存器类型选择读取方法
        if reg_type == 'coil':
            rr = client.read_coils(address=addr, count=count, device_id=unit)
        elif reg_type == 'discrete':
            rr = client.read_discrete_inputs(address=addr, count=count, device_id=unit)
        elif reg_type == 'input':
            rr = client.read_input_registers(address=addr, count=count, device_id=unit)
        else:  # holding
            rr = client.read_holding_registers(address=addr, count=count, device_id=unit)
        
        client.close()
        
        if rr is None:
            return None
            
        if isinstance(rr, ExceptionResponse):
            print(f"Modbus异常响应: {rr}")
            return None
            
        return rr
    except ModbusException as e:
        print(f"Modbus通信错误: {e}")
        return None
    except Exception as e:
        print(f"其他错误: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Modbus读取测试工具")
    parser.add_argument("--mode", choices=["tcp","rtu"], required=True, help="通信模式")
    parser.add_argument("--host", help="TCP模式下的主机地址")    
    parser.add_argument("--port", type=int, default=502, help="TCP模式下的端口号") 
    parser.add_argument("--serial-port", dest="serial_port", help="RTU模式下的串口设备路径") 
    parser.add_argument("--baud", type=int, default=9600, help="RTU模式下的波特率")
    parser.add_argument("--parity", default='N', choices=['N','E','O'], help="RTU模式下的奇偶校验")
    parser.add_argument("--stopbits", type=int, default=1, choices=[1,2], help="RTU模式下的停止位")
    parser.add_argument("--unit", type=int, default=1, help="Modbus单元ID/从站地址")
    parser.add_argument("--addr", type=int, required=True, help="寄存器地址")
    parser.add_argument("--count", type=int, default=1, help="读取寄存器数量")
    parser.add_argument("--type", default='holding', choices=['coil', 'discrete', 'input', 'holding'], 
                       help="读取的寄存器类型")
    parser.add_argument("--timeout", type=float, default=3.0, help="通信超时时间（秒）")
    
    args = parser.parse_args()

    if args.mode == "tcp":
        if not args.host:
            print("错误: TCP模式需要指定--host参数")
            sys.exit(1)
        result = read_modbus_tcp(
            args.host, args.port, args.unit, args.addr, 
            args.count, args.type, args.timeout
        )
    else:
        if not args.serial_port:
            print("错误: RTU模式需要指定--serial-port参数")
            sys.exit(1)
        result = read_modbus_rtu(
            args.serial_port, args.baud, args.parity, args.stopbits, 
            args.unit, args.addr, args.count, args.type, args.timeout
        )

    if result is None:
        print("读取失败：无响应或无法连接")
        sys.exit(1)
    elif hasattr(result, "isError") and result.isError():
        print(f"Modbus错误: {result}")
        sys.exit(1)
    elif hasattr(result, "registers"):
        print(f"读取成功，寄存器值: {result.registers}")
        if len(result.registers) == 1:
            print(f"单个寄存器值 (整数): {result.registers[0]}")
    elif hasattr(result, "bits"):
        print(f"读取成功，线圈/离散输入值: {result.bits}")
        if len(result.bits) == 1:
            print(f"单个位值 (布尔): {bool(result.bits[0])}")
    else:
        print(f"读取响应: {result}")
    
if __name__ == "__main__":
    main()