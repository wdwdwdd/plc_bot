#!/bin/bash

# 停止当前运行的服务
echo "停止现有服务..."
docker-compose down

# 拉取最新代码
echo "更新代码..."
git pull origin master

# 构建新镜像
echo "构建Docker镜像..."
docker-compose build

# 执行数据库迁移
echo "执行数据库迁移..."
python scripts/init_db.py

# 启动服务
echo "启动服务..."
docker-compose up -d

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

# 检查日志
echo "检查服务日志..."
docker-compose logs --tail=100

echo "部署完成！"
