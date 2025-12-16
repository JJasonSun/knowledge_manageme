"""
关系模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class RelationType(enum.Enum):
    """关系类型枚举"""
    SYNONYM = "synonym"
    ANTONYM = "antonym"


class ChengyuRelation(Base):
    """成语关系模型"""
    __tablename__ = "chengyu_relation"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    min_id = Column(Integer, nullable=False, index=True, comment="最小ID")
    max_id = Column(Integer, nullable=False, index=True, comment="最大ID")
    relation_type = Column(Enum(RelationType), nullable=False, comment="关系类型")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<ChengyuRelation(id={self.id}, min_id={self.min_id}, max_id={self.max_id}, type={self.relation_type})>"


class CiyuRelation(Base):
    """词语关系模型"""
    __tablename__ = "ciyu_relation"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    min_id = Column(Integer, nullable=False, index=True, comment="最小ID")
    max_id = Column(Integer, nullable=False, index=True, comment="最大ID")
    relation_type = Column(Enum(RelationType), nullable=False, comment="关系类型")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<CiyuRelation(id={self.id}, min_id={self.min_id}, max_id={self.max_id}, type={self.relation_type})>"