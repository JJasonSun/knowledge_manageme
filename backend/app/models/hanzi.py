"""
汉字模型
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Hanzi(Base):
    """汉字模型，包含汉字的详细信息"""
    __tablename__ = "hanyuguoxue_hanzi"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    character = Column(String(10), unique=True, nullable=False, index=True, comment="汉字")
    url = Column(String(500), nullable=True, comment="URL链接")
    unicode_decimal = Column(Integer, nullable=True, index=True, comment="Unicode十进制")
    basic_info = Column(JSON, nullable=True, comment="基本信息")
    gaishu_info = Column(JSON, nullable=True, comment="概述信息")
    yisi_info = Column(JSON, nullable=True, comment="意思信息")
    fanyi_info = Column(JSON, nullable=True, comment="翻译信息")
    guoyu_info = Column(JSON, nullable=True, comment="国语信息")
    liangan_info = Column(JSON, nullable=True, comment="两岸信息")
    evolution_data = Column(JSON, nullable=True, comment="演变数据")
    error = Column(Text, nullable=True, comment="错误信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Hanzi(id={self.id}, character='{self.character}')>"