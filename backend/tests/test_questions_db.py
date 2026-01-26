import sys
import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 添加 backend 目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.core.database import get_questions_db, QuestionsSessionLocal

def test_questions_connection():
    """
    测试 Questions DB (PostgreSQL) 连接
    """
    print("\n[测试] 正在连接 PostgreSQL 数据库...")
    
    try:
        # 获取 DB Session
        if not QuestionsSessionLocal:
            print("[错误] QuestionsSessionLocal 未初始化。请检查 SSH 隧道和数据库配置。")
            assert False, "QuestionsSessionLocal 未初始化"

        db = QuestionsSessionLocal()
        
        # 执行简单查询
        result = db.execute(text("SELECT 1")).scalar()
        print(f"[成功] 数据库连接成功，查询结果: {result}")
        assert result == 1
        
        # 检查 exercises 表是否存在
        result = db.execute(text("SELECT table_schema FROM information_schema.tables WHERE table_name = 'exercises'")).fetchall()
        if result:
            print(f"[成功] exercises 表存在于 schema: {[r[0] for r in result]}")
        else:
            print("[警告] exercises 表不存在！请检查数据库 schema。")
            # 检查所有表
            tables = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")).fetchall()
            print(f"[信息] public schema 下的表: {[r[0] for r in tables]}")
            
            # 检查 content_system schema
            tables = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'content_system'")).fetchall()
            if tables:
                print(f"[信息] content_system schema 下的表: {[r[0] for r in tables]}")
        
        db.close()
        
    except Exception as e:
        print(f"[失败] 连接或查询失败: {e}")
        assert False, f"连接或查询失败: {e}"

if __name__ == "__main__":
    test_questions_connection()
