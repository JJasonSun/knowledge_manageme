"""
测试数据库连接脚本
同时显示数据库中的表及其记录数，并执行一些基本查询以验证连接有效性
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import test_connection, engine
from sqlalchemy import text


def test_database_connection():
    """
    测试数据库连接并显示现有表
    """
    print("开始测试数据库连接...")
    
    # 基本连接测试
    try:
        # 直接测试连接
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ 数据库连接成功")
            
            # 获取数据库中的所有表
            result = connection.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            
            print(f"\n📋 数据库中的表 ({len(tables)}个):")
            for i, table in enumerate(tables, 1):
                table_name = table[0]
                print(f"  {i}. {table_name}")
                
                # 获取表的记录数
                try:
                    count_result = connection.execute(text(f"SELECT COUNT(*) FROM `{table_name}`"))
                    count = count_result.fetchone()[0]
                    print(f"     记录数: {count:,}")
                except Exception as e:
                    print(f"     无法获取记录数: {e}")
            
            # 测试一些基本查询
            print("\n🔍 测试基本数据查询:")
            
            # 如果有成语表，测试查询
            table_names = [table[0] for table in tables]
            
            if 'idiom' in table_names or 'idioms' in table_names:
                table_name = 'idiom' if 'idiom' in table_names else 'idioms'
                try:
                    sample_result = connection.execute(text(f"SELECT * FROM `{table_name}` LIMIT 3"))
                    samples = sample_result.fetchall()
                    print(f"  {table_name} 表示例数据:")
                    for sample in samples:
                        print(f"    {sample}")
                except Exception as e:
                    print(f"    查询 {table_name} 表失败: {e}")
            
            if 'word' in table_names or 'words' in table_names:
                table_name = 'word' if 'word' in table_names else 'words'
                try:
                    count_result = connection.execute(text(f"SELECT COUNT(*) FROM `{table_name}`"))
                    count = count_result.fetchone()[0]
                    print(f"  {table_name} 表记录数: {count:,}")
                except Exception as e:
                    print(f"    查询 {table_name} 表失败: {e}")
                    
    except Exception as e:
        print(f"❌ 查询数据库表失败: {e}")
        return False
    
    print("\n✅ 数据库连接测试完成")
    return True


if __name__ == "__main__":
    test_database_connection()