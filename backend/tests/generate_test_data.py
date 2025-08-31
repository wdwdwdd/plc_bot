#!/usr/bin/env python3
# generate_test_data.py
# 生成模拟的 PLC 测试数据并存储到 Redis

import redis
import random

# Redis 配置
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# PLC 继电器地址范围
RELAY_START = 0
RELAY_END = 100

# 连接到 Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def generate_relay_data():
    """生成继电器测试数据"""
    for address in range(RELAY_START, RELAY_END + 1):
        # 随机生成继电器状态（ON/OFF）
        status = random.randint(0, 1)
        redis_client.set(f"plc:relay:{address}", status)
        print(f"Generated relay {address}: {'ON' if status else 'OFF'}")

if __name__ == "__main__":
    print("Generating PLC test data...")
    generate_relay_data()
    print("Test data generation completed.")