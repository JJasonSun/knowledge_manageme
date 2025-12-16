"""
测试SQLAlchemy模型
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import inspect
from app.core.database import engine
from app.models import Chengyu, Ciyu, Hanzi, ChengyuRelation, CiyuRelation, User


def test_models():
    """测试模型是否正确映射到数据库表"""
    print("🔍 测试SQLAlchemy模型...")
    
    inspector = inspect(engine)
    
    # 测试成语模型
    print("\n=== 测试成语模型 ===")
    try:
        chengyu_columns = inspector.get_columns("hanyuguoxue_chengyu")
        print(f"✅ 成语表字段数量: {len(chengyu_columns)}")
        model_columns = [column.name for column in Chengyu.__table__.columns]
        db_columns = [col['name'] for col in chengyu_columns]
        print(f"📋 模型字段: {model_columns}")
        print(f"📋 数据库字段: {db_columns}")
        print(f"✅ 字段匹配: {set(model_columns) == set(db_columns)}")
    except Exception as e:
        print(f"❌ 成语模型测试失败: {e}")
    
    # 测试词语模型
    print("\n=== 测试词语模型 ===")
    try:
        ciyu_columns = inspector.get_columns("hanyuguoxue_ciyu")
        print(f"✅ 词语表字段数量: {len(ciyu_columns)}")
        model_columns = [column.name for column in Ciyu.__table__.columns]
        db_columns = [col['name'] for col in ciyu_columns]
        print(f"📋 模型字段: {model_columns}")
        print(f"📋 数据库字段: {db_columns}")
        print(f"✅ 字段匹配: {set(model_columns) == set(db_columns)}")
    except Exception as e:
        print(f"❌ 词语模型测试失败: {e}")
    
    # 测试汉字模型
    print("\n=== 测试汉字模型 ===")
    try:
        hanzi_columns = inspector.get_columns("hanyuguoxue_hanzi")
        print(f"✅ 汉字表字段数量: {len(hanzi_columns)}")
        model_columns = [column.name for column in Hanzi.__table__.columns]
        db_columns = [col['name'] for col in hanzi_columns]
        print(f"📋 模型字段: {model_columns}")
        print(f"📋 数据库字段: {db_columns}")
        print(f"✅ 字段匹配: {set(model_columns) == set(db_columns)}")
    except Exception as e:
        print(f"❌ 汉字模型测试失败: {e}")
    
    # 测试关系模型
    print("\n=== 测试关系模型 ===")
    try:
        chengyu_relation_columns = inspector.get_columns("chengyu_relation")
        print(f"✅ 成语关系表字段数量: {len(chengyu_relation_columns)}")
        model_columns = [column.name for column in ChengyuRelation.__table__.columns]
        db_columns = [col['name'] for col in chengyu_relation_columns]
        print(f"📋 模型字段: {model_columns}")
        print(f"📋 数据库字段: {db_columns}")
        print(f"✅ 字段匹配: {set(model_columns) == set(db_columns)}")
    except Exception as e:
        print(f"❌ 成语关系模型测试失败: {e}")
    
    # 测试数据查询
    print("\n=== 测试数据查询 ===")
    try:
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        # 查询成语数量
        chengyu_count = session.query(Chengyu).count()
        print(f"📊 成语数量: {chengyu_count:,}")
        
        # 查询词语数量
        ciyu_count = session.query(Ciyu).count()
        print(f"📊 词语数量: {ciyu_count:,}")
        
        # 查询汉字数量
        hanzi_count = session.query(Hanzi).count()
        print(f"📊 汉字数量: {hanzi_count:,}")
        
        # 查询第一个成语
        first_chengyu = session.query(Chengyu).first()
        if first_chengyu:
            print(f"🔤 第一个成语: {first_chengyu.chengyu}")
            print(f"📝 拼音: {first_chengyu.pinyin}")
            print(f"💡 解释: {first_chengyu.explanation[:50]}..." if first_chengyu.explanation else "💡 解释: 无")
        
        session.close()
        print("✅ 数据查询测试成功")
        
    except Exception as e:
        print(f"❌ 数据查询测试失败: {e}")
    
    print("\n✅ 模型测试完成")


if __name__ == "__main__":
    test_models()