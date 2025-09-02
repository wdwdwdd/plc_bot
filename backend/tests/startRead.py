from pymodbus.client import ModbusTcpClient

# PLC 参数
PLC_IP = "192.168.1.61"
PLC_PORT = 502
UNIT_ID = 1  # 一般保持 1 即可

# 建立 Modbus TCP 客户端
client = ModbusTcpClient(host=PLC_IP, port=PLC_PORT)

if client.connect():
    # 读取 Y0 ~ Y7 （共 8 个 coil，从索引 0 开始）
    result = client.read_coils(address=0, count=8, unit=UNIT_ID)

    if not result.isError():
        for i, state in enumerate(result.bits):
            print(f"Y{i}: {'ON' if state else 'OFF'}")
    else:
        print("读取失败，可能是地址不对或通信错误。")

    client.close()
else:
    print("无法连接到 PLC，请检查 IP/端口。")
