"""
汉字相关的Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class HanziBase(BaseModel):
    """汉字基础信息"""
    character: str
    url: Optional[str] = None
    unicode_decimal: Optional[int] = None
    basic_info: Optional[Dict[str, Any]] = None
    gaishu_info: Optional[Dict[str, Any]] = None
    yisi_info: Optional[Dict[str, Any]] = None
    fanyi_info: Optional[Dict[str, Any]] = None
    guoyu_info: Optional[Dict[str, Any]] = None
    liangan_info: Optional[Dict[str, Any]] = None
    evolution_data: Optional[Dict[str, Any]] = None


class HanziCreate(HanziBase):
    """创建汉字请求"""
    created_by: Optional[str] = None


class HanziUpdate(BaseModel):
    """更新汉字请求"""
    character: Optional[str] = None
    url: Optional[str] = None
    unicode_decimal: Optional[int] = None
    basic_info: Optional[Dict[str, Any]] = None
    gaishu_info: Optional[Dict[str, Any]] = None
    yisi_info: Optional[Dict[str, Any]] = None
    fanyi_info: Optional[Dict[str, Any]] = None
    guoyu_info: Optional[Dict[str, Any]] = None
    liangan_info: Optional[Dict[str, Any]] = None
    created_by: Optional[str] = None
    evolution_data: Optional[Dict[str, Any]] = None


class HanziResponse(HanziBase):
    """汉字响应"""
    id: int
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HanziListResponse(BaseModel):
    """汉字列表响应"""
    items: List[HanziResponse]
    total: int
    page: int
    size: int
    pages: int
