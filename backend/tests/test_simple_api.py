"""
简单的API测试脚本
利用SQLAlchemy执行基本查询以验证数据库连接有效性
导入自定义的模型以确保它们正确映射到数据库表
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models import Chengyu, Ciyu, Hanzi


def test_simple_queries():
    """测试简单的数据库查询"""
    print("🔍 测试简单数据库查询...")
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        # 测试成语查询
        print("\n=== 成语查询测试 ===")
        chengyu_count = session.query(Chengyu).count()
        print(f"📊 成语总数: {chengyu_count:,}")
        
        # 查询包含"爱"字的成语
        love_chengyu = session.query(Chengyu).filter(Chengyu.chengyu.like('%爱%')).limit(5).all()
        print(f"💕 包含'爱'字的成语({len(love_chengyu)}个):")
        for chengyu in love_chengyu:
            print(f"  - {chengyu.chengyu} ({chengyu.pinyin})")
        
        # 测试词语查询
        print("\n=== 词语查询测试 ===")
        ciyu_count = session.query(Ciyu).count()
        print(f"📊 词语总数: {ciyu_count:,}")
        
        # 查询常用词语
        common_words = session.query(Ciyu).filter(Ciyu.is_common == True).limit(5).all()
        print(f"⭐ 常用词语({len(common_words)}个):")
        for word in common_words:
            print(f"  - {word.word} ({word.pinyin}) - {word.part_of_speech}")
        
        # 测试汉字查询
        print("\n=== 汉字查询测试 ===")
        hanzi_count = session.query(Hanzi).count()
        print(f"📊 汉字总数: {hanzi_count:,}")
        
        # 查询所有汉字
        all_hanzi = session.query(Hanzi).all()
        print(f"🔤 所有汉字({len(all_hanzi)}个):")
        for hanzi in all_hanzi:
            print(f"  - {hanzi.character} (Unicode: {hanzi.unicode_decimal})")
        
        print("\n✅ 所有查询测试成功")
        
    except Exception as e:
        print(f"❌ 查询测试失败: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    test_simple_queries()