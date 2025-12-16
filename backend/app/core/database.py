from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 创建数据库引擎，后续可以使用该引擎与数据库交互，sessionmaker(bind=engine)用于创建数据库会话
engine = create_engine(
    settings.DATABASE_URL, # 数据库连接URL
    echo=settings.DEBUG,  # 在调试模式下打印SQL语句
    pool_pre_ping=True,   # 连接池预检查
    pool_recycle=3600,    # 连接回收时间（秒）
)

# 创建会话工厂，用于生成数据库会话，绑定到引擎，不自动提交和刷新，确保数据一致性
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    可以在FastAPI的依赖注入中使用
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    """
    测试数据库连接
    """
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print(f"数据库连接成功: {result.fetchone()}")
            return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False