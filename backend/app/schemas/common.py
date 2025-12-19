"""
通用的API响应schemas
"""
from pydantic import BaseModel
from typing import Optional, Any, List, Generic, TypeVar


T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """通用API响应"""
    success: bool = True
    message: str = "操作成功"
    data: Optional[T] = None
    code: int = 200


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = False
    message: str
    code: int
    details: Optional[Any] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


class SearchParams(BaseModel):
    """搜索参数"""
    keyword: Optional[str] = None
    page: int = 1
    size: int = 20
    sort_by: Optional[str] = None
    order: Optional[str] = "desc"