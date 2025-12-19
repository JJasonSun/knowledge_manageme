"""
成语相关的Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class ChengyuBase(BaseModel):
    """成语基础信息"""
    chengyu: str
    pinyin: Optional[str] = None
    zhuyin: Optional[str] = None
    emotion: Optional[str] = None
    explanation: Optional[str] = None
    source: Optional[str] = None
    usage: Optional[str] = None
    example: Optional[str] = None
    synonyms: Optional[Dict[str, Any]] = None
    antonyms: Optional[Dict[str, Any]] = None
    translation: Optional[str] = None


class ChengyuCreate(ChengyuBase):
    """创建成语请求"""
    pass


class ChengyuUpdate(BaseModel):
    """更新成语请求"""
    chengyu: Optional[str] = None
    pinyin: Optional[str] = None
    zhuyin: Optional[str] = None
    emotion: Optional[str] = None
    explanation: Optional[str] = None
    source: Optional[str] = None
    usage: Optional[str] = None
    example: Optional[str] = None
    synonyms: Optional[Dict[str, Any]] = None
    antonyms: Optional[Dict[str, Any]] = None
    translation: Optional[str] = None


class ChengyuResponse(ChengyuBase):
    """成语响应"""
    id: int
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChengyuListResponse(BaseModel):
    """成语列表响应"""
    items: List[ChengyuResponse]
    total: int
    page: int
    size: int
    pages: int