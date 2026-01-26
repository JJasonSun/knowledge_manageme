import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Add backend to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.core.database import get_questions_db

client = TestClient(app)

def test_get_questions_api():
    """
    测试获取题目列表 API
    """
    print("\n[测试] GET /api/v1/questions")
    
    response = client.get("/api/v1/questions?page=1&size=5")
    
    if response.status_code != 200:
        print(f"[失败] 状态码: {response.status_code}")
        print(f"[失败] 响应: {response.text}")
    else:
        print(f"[成功] 状态码: 200")
        data = response.json()
        print(f"[信息] 返回数据结构: keys={list(data.keys())}")
        print(f"[信息] 题目数量: {len(data['items'])}")
        print(f"[信息] 总数: {data['total']}")
        
        if len(data['items']) > 0:
            print(f"[信息] 第一题示例: {data['items'][0]}")

    assert response.status_code == 200
    assert "items" in response.json()
    assert "total" in response.json()

def test_get_question_detail_api():
    """
    测试获取单个题目详情 API (需要先获取一个 ID)
    """
    # 先获取列表
    response = client.get("/api/v1/questions?size=1")
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            question_id = data['items'][0]['id']
            print(f"\n[测试] GET /api/v1/questions/{question_id}")
            
            detail_response = client.get(f"/api/v1/questions/{question_id}")
            
            if detail_response.status_code == 200:
                print(f"[成功] 获取详情成功")
                print(f"[信息] 详情: {detail_response.json()}")
            else:
                print(f"[失败] 获取详情失败: {detail_response.status_code}")
                print(f"[失败] 响应: {detail_response.text}")
            
            assert detail_response.status_code == 200
            assert detail_response.json()['id'] == question_id
        else:
            print("\n[跳过] 没有题目数据，跳过详情测试")
    else:
        print("\n[失败] 无法获取列表，跳过详情测试")

if __name__ == "__main__":
    test_get_questions_api()
    test_get_question_detail_api()
