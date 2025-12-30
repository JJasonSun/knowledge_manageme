"""
查看数据库表结构
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine
from sqlalchemy import text

TABLES = [
    "hanyuguoxue_chengyu",
    "hanyuguoxue_ciyu",
    "chengyu_relation",
    "ciyu_relation",
    "hanyuguoxue_hanzi",
    "hsk_word",
]


def print_table_details(conn, table_name, sample_limit=3):
    print(f'=== {table_name} 表结构 ===')
    result = conn.execute(text(f'DESCRIBE {table_name}'))
    for row in result:
        field = row[0] or ""
        type_str = row[1] or ""
        null = row[2] or ""
        key = row[3] or ""
        default = str(row[4]) if row[4] is not None else ""
        extra = row[5] or ""
        print(f'{field:20} {type_str:15} {null:5} {key:5} {default:10} {extra}')
    print_sample_rows(conn, table_name, sample_limit)


def print_sample_rows(conn, table_name, limit):
    print(f'--- 前{limit}条数据样例 ---')
    sample_result = conn.execute(text(f'SELECT * FROM {table_name} LIMIT {limit}'))
    columns = sample_result.keys()
    rows = sample_result.fetchall()
    if not rows:
        print('表中暂无数据样例。')
        return

    header = ' | '.join(columns)
    print(header)
    for row in rows:
        values = ' | '.join(str(value) if value is not None else '' for value in row)
        print(values)


def check_table_structure():
    with engine.connect() as conn:
        for index, table_name in enumerate(TABLES):
            if index:
                print()
            print_table_details(conn, table_name)


if __name__ == "__main__":
    check_table_structure()