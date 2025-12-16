"""
成语模型
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base


class Chengyu(Base):
    """成语模型"""
    __tablename__ = "hanyuguoxue_chengyu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chengyu = Column(String(50), unique=True, nullable=False, index=True, comment="成语")
    url = Column(Text, nullable=True, comment="URL链接")
    pinyin = Column(String(200), nullable=True, comment="拼音")
    zhuyin = Column(String(200), nullable=True, comment="注音")
    emotion = Column(String(50), nullable=True, comment="情感色彩")
    explanation = Column(Text, nullable=True, comment="解释")
    source = Column(Text, nullable=True, comment="来源")
    usage = Column(Text, nullable=True, comment="用法")
    example = Column(Text, nullable=True, comment="例句")
    synonyms = Column(JSON, nullable=True, comment="同义词")
    antonyms = Column(JSON, nullable=True, comment="反义词")
    translation = Column(Text, nullable=True, comment="翻译")
    error = Column(Text, nullable=True, comment="错误信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Chengyu(id={self.id}, chengyu='{self.chengyu}')>"