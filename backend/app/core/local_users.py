"""
本地用户管理（不使用数据库）
"""
import sys
import os
from typing import Optional, Dict, Any

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from app.core.security import verify_password
from app.schemas.user import UserResponse, TokenData


class LocalUser:
    """本地用户类"""
    def __init__(self, id: int, username: str, hashed_password: str, role: str):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.role = role
    
    def __repr__(self):
        return f"<LocalUser(id={self.id}, username='{self.username}', role='{self.role}')>"


# 硬编码用户列表
LOCAL_USERS: Dict[str, LocalUser] = {
    "admin": LocalUser(
        id=1,
        username="admin",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHGNO.yHzJQ5VRMahO8I.K.1.TTo8pRVJ9G",  # "admin123"的哈希
        role="admin"
    ),
    "teacher": LocalUser(
        id=2,
        username="teacher",  
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31l",  # "teach123"的哈希
        role="teacher"
    )
}


def get_local_user_by_username(username: str) -> Optional[LocalUser]:
    """根据用户名获取本地用户"""
    return LOCAL_USERS.get(username)


def authenticate_local_user(username: str, password: str) -> Optional[LocalUser]:
    """验证本地用户"""
    user = get_local_user_by_username(username)
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def create_user_response(user: LocalUser) -> UserResponse:
    """从本地用户创建用户响应"""
    return UserResponse(
        id=user.id,
        username=user.username,
        role=user.role
    )


def create_token_data(user: LocalUser) -> TokenData:
    """从本地用户创建token数据"""
    return TokenData(
        username=user.username,
        role=user.role
    )


def get_all_local_users_info() -> Dict[str, Any]:
    """获取所有本地用户信息（不包含密码）"""
    return {
        username: {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
        for username, user in LOCAL_USERS.items()
    }


# 测试函数
def test_local_users():
    """测试本地用户功能"""
    print("🔍 测试本地用户功能...")
    
    # 测试正确的登录
    admin_user = authenticate_local_user("admin", "admin123")
    if admin_user:
        print(f"✅ 管理员登录成功: {admin_user}")
    else:
        print("❌ 管理员登录失败")
    
    # 测试错误的密码
    admin_wrong = authenticate_local_user("admin", "wrong_password")
    if admin_wrong:
        print(f"❌ 错误密码应该失败: {admin_wrong}")
    else:
        print("✅ 错误密码验证正确")
    
    # 测试不存在的用户
    no_user = authenticate_local_user("ghost", "password")
    if no_user:
        print(f"❌ 不存在用户应该失败: {no_user}")
    else:
        print("✅ 不存在用户验证正确")
    
    # 测试用户信息
    print(f"\n📋 所有用户信息:")
    all_info = get_all_local_users_info()
    for username, info in all_info.items():
        print(f"  {username}: {info}")


if __name__ == "__main__":
    test_local_users()