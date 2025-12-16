"""
词语模型
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Ciyu(Base):
    """词语模型，包含词语的详细信息"""
    __tablename__ = "hanyuguoxue_ciyu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String(100), unique=True, nullable=False, index=True, comment="词语")
    url = Column(Text, nullable=True, comment="URL链接")
    pinyin = Column(String(200), nullable=True, comment="拼音")
    zhuyin = Column(String(200), nullable=True, comment="注音")
    part_of_speech = Column(String(50), nullable=True, index=True, comment="词性")
    is_common = Column(Boolean, default=False, nullable=True, comment="是否常用")
    definition = Column(Text, nullable=True, comment="定义")
    synonyms = Column(JSON, nullable=True, comment="同义词")
    antonyms = Column(JSON, nullable=True, comment="反义词")
    error = Column(Text, nullable=True, comment="错误信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Ciyu(id={self.id}, word='{self.word}')>"