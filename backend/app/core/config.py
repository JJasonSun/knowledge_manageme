from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str
    
    # JWT配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # 应用配置
    APP_NAME: str = "中文教育资源管理系统"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # CORS配置
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    class Config:
        # 获取backend目录的绝对路径，然后指向.env文件
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")


settings = Settings()