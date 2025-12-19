"""
简单的本地认证模块（硬编码用户）
"""
import sys
import os
from typing import Optional, Dict
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.config import settings


class SimpleUser(BaseModel):
    """简单用户模型"""
    id: int
    username: str
    password: str  # 注意：实际应用中应该存储哈希值
    role: str


# 硬编码用户列表
LOCAL_USERS = {
    "admin": SimpleUser(id=1, username="admin", password="admin123", role="admin"),
    "teacher": SimpleUser(id=2, username="teacher", password="teach123", role="teacher")
}


def authenticate_user(username: str, password: str) -> Optional[SimpleUser]:
    """验证用户"""
    user = LOCAL_USERS.get(username)
    if user and user.password == password:
        return user
    return None


def get_user_by_username(username: str) -> Optional[SimpleUser]:
    """根据用户名获取用户"""
    return LOCAL_USERS.get(username)


def create_access_token(username: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT访问令牌"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": username,
        "role": role,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict]:
    """验证JWT令牌"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception:
        return None


def check_admin_permission(role: str) -> bool:
    """检查管理员权限"""
    return role == "admin"


def check_teacher_or_admin_permission(role: str) -> bool:
    """检查老师或管理员权限"""
    return role in ["admin", "teacher"]


# HTTP Bearer认证实例
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """获取当前用户（FastAPI依赖）"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 验证token
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        username: str = payload.get("sub")
        role: str = payload.get("role")
        
        if username is None or role is None:
            raise credentials_exception
            
        # 获取用户信息
        user = get_user_by_username(username)
        if user is None:
            raise credentials_exception
            
        return user
        
    except Exception:
        raise credentials_exception


async def get_current_admin_user(current_user: SimpleUser = Depends(get_current_user)):
    """获取当前管理员用户（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限"
        )
    return current_user


async def get_current_teacher_or_admin_user(current_user: SimpleUser = Depends(get_current_user)):
    """获取当前老师或管理员用户（需要老师或管理员权限）"""
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要老师或管理员权限"
        )
    return current_user


if __name__ == "__main__":
    # 测试简单认证
    print("🔍 测试简单认证...")
    
    # 测试用户验证
    user = authenticate_user("admin", "admin123")
    print(f"✅ 管理员验证: {user.username if user else '失败'}")
    
    user = authenticate_user("teacher", "teach123")
    print(f"✅ 老师验证: {user.username if user else '失败'}")
    
    user = authenticate_user("wrong", "wrong")
    print(f"❌ 错误用户验证: {user.username if user else '失败'}")
    
    # 测试Token生成
    token = create_access_token("admin", "admin")
    print(f"✅ Token生成: {token[:50]}...")
    
    # 测试Token验证
    payload = verify_token(token)
    print(f"✅ Token验证: {payload}")
    
    # 测试权限
    print(f"✅ 管理员权限: {check_admin_permission('admin')}")
    print(f"✅ 老师权限: {check_teacher_or_admin_permission('teacher')}")
    print(f"❌ 访客权限: {check_admin_permission('guest')}")