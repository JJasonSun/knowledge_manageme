"""
用户模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    email = Column(String(100), unique=True, nullable=False, index=True, comment="邮箱")
    hashed_password = Column(String(255), nullable=False, comment="加密密码")
    role = Column(String(20), nullable=False, default="teacher", comment="角色 (admin/teacher)")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")
    full_name = Column(String(100), nullable=True, comment="全名")
    avatar_url = Column(String(500), nullable=True, comment="头像URL")
    description = Column(Text, nullable=True, comment="个人描述")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    last_login = Column(DateTime(timezone=True), nullable=True, comment="最后登录时间")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"