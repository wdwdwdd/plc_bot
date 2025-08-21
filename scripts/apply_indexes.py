import sys
import os
import yaml
from sqlalchemy import create_engine, text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.database import load_db_config


def main():
    cfg = load_db_config()
    url = f"postgresql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['name']}"
    engine = create_engine(url)
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'models', 'indexes.sql')
    sql_path = os.path.abspath(sql_path)
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    with engine.begin() as conn:
        for stmt in [s.strip() for s in sql.split(';') if s.strip()]:
            conn.execute(text(stmt))
    print('Indexes applied.')


if __name__ == '__main__':
    main()

