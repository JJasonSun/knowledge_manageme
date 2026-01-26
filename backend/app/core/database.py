from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import atexit

# Global variable to hold the tunnel
ssh_tunnel = None

# ================= Primary Database (MySQL) =================
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=3600,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ================= Secondary Database (PostgreSQL via SSH) =================
questions_engine = None
QuestionsSessionLocal = None

if settings.SSH_HOST:
    try:
        from sshtunnel import SSHTunnelForwarder
        
        print(f"Connecting to SSH Tunnel: {settings.SSH_HOST}...")
        ssh_tunnel = SSHTunnelForwarder(
            (settings.SSH_HOST, settings.SSH_PORT),
            ssh_username=settings.SSH_USER,
            ssh_password=settings.SSH_PASSWORD,
            remote_bind_address=(settings.QUESTIONS_DB_HOST, settings.QUESTIONS_DB_PORT)
        )
        ssh_tunnel.start()
        print(f"SSH Tunnel established on port {ssh_tunnel.local_bind_port}")
        
        # Construct Questions DB URL
        questions_db_url = f"postgresql+psycopg2://{settings.QUESTIONS_DB_USER}:{settings.QUESTIONS_DB_PASSWORD}@127.0.0.1:{ssh_tunnel.local_bind_port}/{settings.QUESTIONS_DB_NAME}"
        
        questions_engine = create_engine(
            questions_db_url,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        QuestionsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=questions_engine)
        
        # Register cleanup
        atexit.register(ssh_tunnel.stop)
        
    except Exception as e:
        print(f"Failed to establish SSH tunnel or connect to Questions DB: {e}")

# 创建基础模型类
Base = declarative_base()
BasePG = declarative_base()


def get_db():
    """
    获取主数据库会话 (MySQL)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_questions_db():
    """
    获取题目数据库会话 (PostgreSQL)
    """
    if not QuestionsSessionLocal:
        raise Exception("Questions database not configured or connection failed")
        
    db = QuestionsSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    """
    测试数据库连接 (Primary MySQL)
    """
    results = {}
    
    # Test MySQL
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"主数据库 (MySQL) 连接成功: {result.fetchone()}")
            results["mysql"] = True
    except Exception as e:
        print(f"主数据库 (MySQL) 连接失败: {e}")
        results["mysql"] = False

    # Test PostgreSQL
    if questions_engine:
        try:
            with questions_engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print(f"次数据库 (PostgreSQL) 连接成功: {result.fetchone()}")
                results["postgresql"] = True
        except Exception as e:
            print(f"次数据库 (PostgreSQL) 连接失败: {e}")
            results["postgresql"] = False
    else:
        print("次数据库 (PostgreSQL) 未配置")
        results["postgresql"] = False

    return results["mysql"] # Return main DB status for backward compatibility check, or check logs for full details


def ensure_owner_columns():
    """确保成语与词语表包含 created_by 字段"""
    tables = [
        ("hanyuguoxue_chengyu", "created_by", "VARCHAR(128)"),
        ("hanyuguoxue_ciyu", "created_by", "VARCHAR(128)"),
        ("hanyuguoxue_hanzi", "created_by", "VARCHAR(128)")
    ]

    try:
        with engine.begin() as connection:
            for table_name, column_name, definition in tables:
                exists_query = text(
                    """
                    SELECT COUNT(*) FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = :table_name
                      AND COLUMN_NAME = :column_name
                    """
                )
                exists = connection.execute(
                    exists_query,
                    {"table_name": table_name, "column_name": column_name}
                ).scalar()

                if exists:
                    continue

                connection.execute(
                    text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")
                )

        return True
    except Exception as e:
        print(f"创建 created_by 列失败: {e}")
        return False