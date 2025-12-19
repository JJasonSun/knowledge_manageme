"""
简化的认证和权限控制装饰器
"""
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.simple_auth import verify_token, get_user_by_username, check_admin_permission, check_teacher_or_admin_permission

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """从token获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    
    return user


async def require_admin(current_user = Depends(get_current_user_from_token)):
    """需要管理员权限的装饰器依赖"""
    if not check_admin_permission(current_user.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限"
        )
    return current_user


async def require_teacher_or_admin(current_user = Depends(get_current_user_from_token)):
    """需要老师或管理员权限的装饰器依赖"""
    if not check_teacher_or_admin_permission(current_user.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要老师或管理员权限"
        )
    return current_user