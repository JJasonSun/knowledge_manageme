"""
测试Pydantic schemas
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas import (
    UserLogin, UserCreate, UserResponse, Token,
    ChengyuCreate, ChengyuResponse, ChengyuListResponse,
    CiyuCreate, CiyuResponse, CiyuListResponse,
    APIResponse, PaginatedResponse, SearchParams
)


def test_user_schemas():
    """测试用户相关schemas"""
    print("🔍 测试用户schemas...")
    
    # 测试登录请求
    login_data = UserLogin(username="admin", password="123456")
    print(f"✅ 登录请求: {login_data}")
    
    # 测试用户创建
    user_create = UserCreate(username="teacher1", password="123456", role="teacher")
    print(f"✅ 用户创建: {user_create}")
    
    # 测试用户响应
    user_response = UserResponse(id=1, username="admin", role="admin")
    print(f"✅ 用户响应: {user_response}")
    
    # 测试Token响应
    token_response = Token(
        access_token="fake_token",
        token_type="bearer",
        user=user_response
    )
    print(f"✅ Token响应: {token_response}")


def test_chengyu_schemas():
    """测试成语相关schemas"""
    print("\n🔍 测试成语schemas...")
    
    # 测试成语创建
    chengyu_create = ChengyuCreate(
        chengyu="画龙点睛",
        pinyin="huà lóng diǎn jīng",
        explanation="比喻写文章或讲话时，在关键处用几句话点明实质"
    )
    print(f"✅ 成语创建: {chengyu_create.chengyu} - {chengyu_create.pinyin}")
    
    # 测试成语响应
    chengyu_response = ChengyuResponse(
        id=1,
        chengyu="画龙点睛",
        pinyin="huà lóng diǎn jīng",
        explanation="比喻写文章或讲话时，在关键处用几句话点明实质"
    )
    print(f"✅ 成语响应: {chengyu_response.chengyu}")


def test_ciyu_schemas():
    """测试词语相关schemas"""
    print("\n🔍 测试词语schemas...")
    
    # 测试词语创建
    ciyu_create = CiyuCreate(
        word="学习",
        pinyin="xué xí",
        part_of_speech="动词",
        definition="获得知识或技能"
    )
    print(f"✅ 词语创建: {ciyu_create.word} - {ciyu_create.part_of_speech}")
    
    # 测试词语响应
    ciyu_response = CiyuResponse(
        id=1,
        word="学习",
        pinyin="xué xí",
        part_of_speech="动词",
        definition="获得知识或技能"
    )
    print(f"✅ 词语响应: {ciyu_response.word}")


def test_common_schemas():
    """测试通用schemas"""
    print("\n🔍 测试通用schemas...")
    
    # 测试API响应
    api_response = APIResponse[str](
        success=True,
        message="操作成功",
        data="成功"
    )
    print(f"✅ API响应: {api_response.message}")
    
    # 测试搜索参数
    search_params = SearchParams(
        keyword="学习",
        page=1,
        size=20
    )
    print(f"✅ 搜索参数: {search_params.keyword}")


def test_schema_validation():
    """测试数据验证"""
    print("\n🔍 测试数据验证...")
    
    try:
        # 测试必填字段验证
        user_login = UserLogin(username="admin")  # 缺少password
        print("❌ 应该验证失败")
    except Exception as e:
        print(f"✅ 验证成功: {e}")
    
    try:
        # 测试正确数据
        user_login = UserLogin(username="admin", password="123456")
        print(f"✅ 验证通过: {user_login.username}")
    except Exception as e:
        print(f"❌ 验证失败: {e}")


if __name__ == "__main__":
    print("🚀 开始测试Pydantic schemas...")
    test_user_schemas()
    test_chengyu_schemas()
    test_ciyu_schemas()
    test_common_schemas()
    test_schema_validation()
    print("\n✅ 所有schemas测试完成！")