#!/bin/bash

# 加载配置
source ../config/settings.yaml

# 备份时间戳
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="../backups"
BACKUP_FILE="${BACKUP_DIR}/plc_monitor_${TIMESTAMP}.sql"

# 创建备份目录
mkdir -p ${BACKUP_DIR}

# 执行备份
pg_dump -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} > ${BACKUP_FILE}

# 压缩备份文件
gzip ${BACKUP_FILE}

# 删除30天前的备份
find ${BACKUP_DIR} -name "*.sql.gz" -mtime +30 -delete

echo "备份完成: ${BACKUP_FILE}.gz"
