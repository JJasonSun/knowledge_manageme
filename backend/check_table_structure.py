"""
查看数据库表结构
"""
from app.core.database import engine
from sqlalchemy import text

def check_table_structure():
    with engine.connect() as conn:
        # 查看成语表结构
        print('=== hanyuguoxue_chengyu 表结构 ===')
        result = conn.execute(text('DESCRIBE hanyuguoxue_chengyu'))
        for row in result:
            field = row[0] or ""
            type_str = row[1] or ""
            null = row[2] or ""
            key = row[3] or ""
            default = str(row[4]) if row[4] is not None else ""
            extra = row[5] or ""
            print(f'{field:20} {type_str:15} {null:5} {key:5} {default:10} {extra}')
        
        print('\n=== hanyuguoxue_ciyu 表结构 ===')
        result = conn.execute(text('DESCRIBE hanyuguoxue_ciyu'))
        for row in result:
            field = row[0] or ""
            type_str = row[1] or ""
            null = row[2] or ""
            key = row[3] or ""
            default = str(row[4]) if row[4] is not None else ""
            extra = row[5] or ""
            print(f'{field:20} {type_str:15} {null:5} {key:5} {default:10} {extra}')

        print('\n=== hanyuguoxue_hanzi 表结构 ===')
        result = conn.execute(text('DESCRIBE hanyuguoxue_hanzi'))
        for row in result:
            field = row[0] or ""
            type_str = row[1] or ""
            null = row[2] or ""
            key = row[3] or ""
            default = str(row[4]) if row[4] is not None else ""
            extra = row[5] or ""
            print(f'{field:20} {type_str:15} {null:5} {key:5} {default:10} {extra}')

if __name__ == "__main__":
    check_table_structure()