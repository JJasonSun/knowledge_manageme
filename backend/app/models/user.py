"""
简化用户模型
"""
from sqlalchemy import Column, Integer, String
from app.core.database import Base


class User(Base):
    """简化用户模型，只包含基本信息"""
    __tablename__ = "users_knma"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    hashed_password = Column(String(255), nullable=False, comment="加密密码")
    role = Column(String(20), nullable=False, default="teacher", comment="角色 (admin/teacher)")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"