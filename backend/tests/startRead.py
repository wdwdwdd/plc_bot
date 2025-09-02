from pymodbus.client import ModbusTcpClient

# PLC 参数
PLC_IP = "192.168.1.61"
PLC_PORT = 502
UNIT_ID = 1  # 一般保持 1 即可

# 建立 Modbus TCP 客户端
plc = ModbusTcpClient(host=PLC_IP, port=PLC_PORT, unit_id=UNIT_ID, auto_open=True)

# 读取 Y0 ~ Y7 （共 8 个 coil，从索引 0 开始）
coils = plc.read_coils(0, 8)

if coils:
    for i, state in enumerate(coils):
        print(f"Y{i}: {'ON' if state else 'OFF'}")
else:
    print("读取失败，请检查连接或地址。")
