"""
用户相关的Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    """用户登录请求"""
    username: str
    password: str


class UserCreate(BaseModel):
    """创建用户请求"""
    username: str
    password: str
    role: str = "teacher"


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT Token响应"""
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    """Token解析数据"""
    username: Optional[str] = None
    role: Optional[str] = None