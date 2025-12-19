"""
FastAPI接口端点测试脚本
测试所有API端点的功能，包括认证、查询、创建等
"""
import requests
import json
from datetime import datetime

class FastAPITester:
    """FastAPI接口测试器"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.admin_token = None
        self.teacher_token = None
        
    def print_test_header(self, test_name):
        """打印测试标题"""
        print(f"\n{'='*60}")
        print(f"🧪 测试: {test_name}")
        print(f"{'='*60}")
    
    def print_result(self, status_code, response_data=None, error_message=None):
        """打印测试结果"""
        print(f"📊 状态码: {status_code}")
        if response_data:
            print(f"📄 响应: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        if error_message:
            print(f"❌ 错误: {error_message}")
    
    def login(self, username, password):
        """用户登录"""
        login_data = {"username": username, "password": password}
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/auth/login", json=login_data)
            if response.status_code == 200:
                token_data = response.json()
                token = token_data["access_token"]
                user_info = token_data["user"]
                print(f"✅ {user_info['username']} 登录成功")
                return token, user_info
            else:
                print(f"❌ {username} 登录失败: {response.text}")
                return None, None
        except Exception as e:
            print(f"❌ 登录请求异常: {e}")
            return None, None
    
    def setup_authentication(self):
        """设置认证令牌"""
        self.print_test_header("用户认证设置")
        
        # 管理员登录
        self.admin_token, admin_info = self.login("admin", "admin123")
        if admin_info:
            print(f"   管理员信息: {admin_info['username']} ({admin_info['role']})")
        
        # 老师登录
        self.teacher_token, teacher_info = self.login("teacher", "teach123")
        if teacher_info:
            print(f"   老师信息: {teacher_info['username']} ({teacher_info['role']})")
    
    def test_health_endpoints(self):
        """测试健康检查端点"""
        self.print_test_header("健康检查端点")
        
        # 测试根路径
        print("\n1. 测试根路径 (/)")
        try:
            response = requests.get(f"{self.base_url}/")
            self.print_result(response.status_code, response.json() if response.status_code == 200 else None)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试健康检查
        print("\n2. 测试健康检查 (/health)")
        try:
            response = requests.get(f"{self.base_url}/health")
            self.print_result(response.status_code, response.json() if response.status_code == 200 else None)
        except Exception as e:
            self.print_result(0, None, str(e))
    
    def test_user_info(self):
        """测试用户信息获取"""
        self.print_test_header("用户信息获取")
        
        if not self.admin_token:
            print("❌ 未获取到管理员令牌，跳过测试")
            return
        
        # 测试管理员信息
        print("\n1. 测试管理员用户信息")
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        try:
            response = requests.get(f"{self.base_url}/api/v1/auth/me", headers=headers)
            self.print_result(response.status_code, response.json() if response.status_code == 200 else None)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试无认证访问
        print("\n2. 测试无认证访问")
        try:
            response = requests.get(f"{self.base_url}/api/v1/auth/me")
            self.print_result(response.status_code, response.json() if response.status_code != 401 else None)
        except Exception as e:
            self.print_result(0, None, str(e))
    
    def test_chengyu_endpoints(self):
        """测试成语管理端点"""
        self.print_test_header("成语管理端点")
        
        if not self.admin_token:
            print("❌ 未获取到管理员令牌，跳过测试")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 测试获取成语列表
        print("\n1. 测试获取成语列表")
        try:
            response = requests.get(f"{self.base_url}/api/v1/chengyu", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 成功获取成语列表")
                print(f"   总数: {data['total']:,}")
                print(f"   当前页: {data['page']}")
                print(f"   返回数量: {len(data['items'])}")
                if data['items']:
                    first_chengyu = data['items'][0]
                    print(f"   第一个成语: {first_chengyu['chengyu']} - {first_chengyu.get('pinyin', 'N/A')}")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试成语搜索
        print("\n2. 测试成语搜索")
        try:
            search_url = f"{self.base_url}/api/v1/chengyu?search=一心&page=1&size=5"
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 搜索成功")
                print(f"   搜索词: '一心'")
                print(f"   结果数量: {len(data['items'])}")
                for item in data['items']:
                    print(f"   - {item['chengyu']}: {item.get('explanation', 'N/A')[:50]}...")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试获取单个成语
        print("\n3. 测试获取单个成语")
        try:
            response = requests.get(f"{self.base_url}/api/v1/chengyu/1", headers=headers)
            if response.status_code == 200:
                chengyu = response.json()
                print(f"✅ 获取单个成语成功")
                print(f"   成语: {chengyu['chengyu']}")
                print(f"   拼音: {chengyu.get('pinyin', 'N/A')}")
                print(f"   解释: {chengyu.get('explanation', 'N/A')[:100]}...")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试创建成语
        print("\n4. 测试创建成语")
        test_chengyu = {
            "chengyu": f"测试成语_{datetime.now().strftime('%H%M%S')}",
            "pinyin": "cè shì chéngyǔ",
            "explanation": "这是通过API创建的测试成语",
            "example": "这是一个测试例句"
        }
        try:
            response = requests.post(f"{self.base_url}/api/v1/chengyu", json=test_chengyu, headers=headers)
            if response.status_code == 200:
                created = response.json()
                print(f"✅ 创建成语成功")
                print(f"   成语ID: {created['id']}")
                print(f"   成语: {created['chengyu']}")
                print(f"   拼音: {created.get('pinyin', 'N/A')}")
            else:
                self.print_result(response.status_code, response.json() if response.headers.get('content-type', '').startswith('application/json') else None)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试无权限创建成语
        print("\n5. 测试无权限创建成语")
        try:
            response = requests.post(f"{self.base_url}/api/v1/chengyu", json=test_chengyu)
            if response.status_code == 401:
                print(f"✅ 权限检查正常，未认证用户无法创建成语")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
    
    def test_ciyu_endpoints(self):
        """测试词语管理端点"""
        self.print_test_header("词语管理端点")
        
        if not self.admin_token:
            print("❌ 未获取到管理员令牌，跳过测试")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 测试获取词语列表
        print("\n1. 测试获取词语列表")
        try:
            response = requests.get(f"{self.base_url}/api/v2/ciyu", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 成功获取词语列表")
                print(f"   总数: {data['total']:,}")
                print(f"   当前页: {data['page']}")
                print(f"   返回数量: {len(data['items'])}")
                if data['items']:
                    first_word = data['items'][0]
                    print(f"   第一个词语: {first_word['word']} - {first_word.get('pinyin', 'N/A')}")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试词语搜索
        print("\n2. 测试词语搜索")
        try:
            search_url = f"{self.base_url}/api/v2/ciyu?search=好&page=1&size=3"
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 搜索成功")
                print(f"   搜索词: '好'")
                print(f"   结果数量: {len(data['items'])}")
                for item in data['items']:
                    print(f"   - {item['word']}: {item.get('definition', 'N/A')[:50]}...")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试获取单个词语
        print("\n3. 测试获取单个词语")
        try:
            response = requests.get(f"{self.base_url}/api/v2/ciyu/1", headers=headers)
            if response.status_code == 200:
                ciyu = response.json()
                print(f"✅ 获取单个词语成功")
                print(f"   词语: {ciyu['word']}")
                print(f"   拼音: {ciyu.get('pinyin', 'N/A')}")
                print(f"   词性: {ciyu.get('part_of_speech', 'N/A')}")
                print(f"   定义: {ciyu.get('definition', 'N/A')[:100]}...")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试创建词语
        print("\n4. 测试创建词语")
        test_ciyu = {
            "word": f"测试词语_{datetime.now().strftime('%H%M%S')}",
            "pinyin": "cè shì cíyǔ",
            "definition": "这是通过API创建的测试词语",
            "part_of_speech": "名词",
            "is_common": False,
            "synonyms": [],
            "antonyms": []
        }
        try:
            response = requests.post(f"{self.base_url}/api/v2/ciyu", json=test_ciyu, headers=headers)
            if response.status_code == 200:
                created = response.json()
                print(f"✅ 创建词语成功")
                print(f"   词语ID: {created['id']}")
                print(f"   词语: {created['word']}")
                print(f"   拼音: {created.get('pinyin', 'N/A')}")
            else:
                self.print_result(response.status_code, response.json() if response.headers.get('content-type', '').startswith('application/json') else None)
        except Exception as e:
            self.print_result(0, None, str(e))
    
    def test_teacher_permissions(self):
        """测试老师权限"""
        self.print_test_header("老师权限测试")
        
        if not self.teacher_token:
            print("❌ 未获取到老师令牌，跳过测试")
            return
        
        headers = {"Authorization": f"Bearer {self.teacher_token}"}
        
        # 测试老师创建成语
        print("\n1. 测试老师创建成语")
        test_chengyu = {
            "chengyu": f"老师测试成语_{datetime.now().strftime('%H%M%S')}",
            "pinyin": "lǎoshī cè shì",
            "explanation": "这是老师创建的测试成语"
        }
        try:
            response = requests.post(f"{self.base_url}/api/v1/chengyu", json=test_chengyu, headers=headers)
            if response.status_code == 200:
                print("✅ 老师成功创建成语")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试老师获取成语列表
        print("\n2. 测试老师获取成语列表")
        try:
            response = requests.get(f"{self.base_url}/api/v1/chengyu", headers=headers)
            if response.status_code == 200:
                print("✅ 老师成功获取成语列表")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
    
    def test_error_cases(self):
        """测试错误情况"""
        self.print_test_header("错误情况测试")
        
        # 测试错误登录
        print("\n1. 测试错误登录")
        login_data = {"username": "wrong", "password": "wrong"}
        try:
            response = requests.post(f"{self.base_url}/api/v1/auth/login", json=login_data)
            if response.status_code == 401:
                print("✅ 错误登录被正确拒绝")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试无效token
        print("\n2. 测试无效token")
        headers = {"Authorization": "Bearer invalid_token"}
        try:
            response = requests.get(f"{self.base_url}/api/v1/auth/me", headers=headers)
            if response.status_code == 401:
                print("✅ 无效token被正确拒绝")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
        
        # 测试不存在的成语
        print("\n3. 测试获取不存在的成语")
        headers = {"Authorization": f"Bearer {self.admin_token}"} if self.admin_token else {}
        try:
            response = requests.get(f"{self.base_url}/api/v1/chengyu/99999", headers=headers)
            if response.status_code == 404:
                print("✅ 不存在的成语返回404")
            else:
                self.print_result(response.status_code)
        except Exception as e:
            self.print_result(0, None, str(e))
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始FastAPI完整测试")
        print(f"📍 测试目标: {self.base_url}")
        print(f"🕐 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 1. 设置认证
            self.setup_authentication()
            
            # 2. 测试健康检查
            self.test_health_endpoints()
            
            # 3. 测试用户信息
            self.test_user_info()
            
            # 4. 测试成语管理
            self.test_chengyu_endpoints()
            
            # 5. 测试词语管理
            self.test_ciyu_endpoints()
            
            # 6. 测试老师权限
            self.test_teacher_permissions()
            
            # 7. 测试错误情况
            self.test_error_cases()
            
            print(f"\n{'='*60}")
            print("✅ 所有FastAPI测试完成!")
            print(f"{'='*60}")
            
        except KeyboardInterrupt:
            print(f"\n⏹️ 测试被用户中断")
        except Exception as e:
            print(f"\n❌ 测试过程中发生异常: {e}")
        
        print(f"\n📊 测试总结:")
        print(f"   管理员认证: {'✅' if self.admin_token else '❌'}")
        print(f"   老师认证: {'✅' if self.teacher_token else '❌'}")
        print(f"   基础端点: [✅/❌] 手动检查上述输出")
        print(f"   业务功能: [✅/❌] 手动检查上述输出")
        print(f"   权限控制: [✅/❌] 手动检查上述输出")
        print(f"   错误处理: [✅/❌] 手动检查上述输出")


def main():
    """主函数"""
    print("🎯 FastAPI接口端点测试工具")
    print("="*60)
    
    # 创建测试器
    tester = FastAPITester("http://localhost:8000")
    
    # 运行所有测试
    tester.run_all_tests()
    
    print(f"\n📖 使用说明:")
    print(f"   1. 确保FastAPI服务在 http://localhost:8000 运行")
    print(f"   2. 检查测试输出中的 ✅ 和 ❌ 标记")
    print(f"   3. 重点关注权限控制和错误处理的测试结果")
    print(f"   4. 查看API响应数据格式和内容正确性")


if __name__ == "__main__":
    main()