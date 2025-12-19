"""
词语相关的Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class CiyuBase(BaseModel):
    """词语基础信息"""
    word: str
    pinyin: Optional[str] = None
    zhuyin: Optional[str] = None
    part_of_speech: Optional[str] = None
    is_common: Optional[bool] = None
    definition: Optional[str] = None
    synonyms: Optional[Dict[str, Any]] = None
    antonyms: Optional[Dict[str, Any]] = None


class CiyuCreate(CiyuBase):
    """创建词语请求"""
    pass


class CiyuUpdate(BaseModel):
    """更新词语请求"""
    word: Optional[str] = None
    pinyin: Optional[str] = None
    zhuyin: Optional[str] = None
    part_of_speech: Optional[str] = None
    is_common: Optional[bool] = None
    definition: Optional[str] = None
    synonyms: Optional[Dict[str, Any]] = None
    antonyms: Optional[Dict[str, Any]] = None


class CiyuResponse(CiyuBase):
    """词语响应"""
    id: int
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CiyuListResponse(BaseModel):
    """词语列表响应"""
    items: List[CiyuResponse]
    total: int
    page: int
    size: int
    pages: int