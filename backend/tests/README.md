# 汉语国学知识管理系统测试文档

## 📋 测试文件概览

本目录包含了完整的测试套件，用于验证汉语国学知识管理系统的各个组件功能。测试分为多个层次，从数据库连接到API端点功能验证。

## 🗂️ 测试文件说明

### 1. `test_db_connection.py` - 数据库连接测试
- **用途**: 验证数据库连接并显示数据库基本信息
- **适用场景**: 
  - 首次部署后的连接验证
  - 数据库故障排查
  - 确认数据库变更好影响
- **测试内容**:
  - 基本连接测试
  - 数据库表列表显示
  - 各表记录数统计
  - 基本SQL查询验证

### 2. `check_table_structure.py` - 数据库表结构查看
- **用途**: 查看和验证数据库表结构
- **适用场景**:
  - 数据库结构验证
  - 开发时查看表字段
  - 模型映射问题排查
- **测试内容**:
  - 成语表结构(hanyuguoxue_chengyu)
  - 词语表结构(hanyuguoxue_ciyu)
  - 成语关系表结构(chengyu_relation)
  - 词语关系表结构(ciyu_relation)

### 3. `test_models.py` - SQLAlchemy模型测试
- **用途**: 测试SQLAlchemy模型与数据库表的映射关系
- **适用场景**:
  - 验证模型定义正确性
  - 检查模型与数据库表字段匹配
  - ORM功能验证
- **测试内容**:
  - 成语模型映射测试
  - 词语模型映射测试
  - 汉字模型映射测试
  - 关系模型映射测试
  - 用户模型映射测试

### 4. `test_schemas.py` - Pydantic模式测试
- **用途**: 测试数据序列化/反序列化模式定义
- **适用场景**:
  - 验证API数据格式
  - 检查数据验证规则
  - 响应格式确认
- **测试内容**:
  - 用户相关schemas(UserLogin, UserCreate, UserResponse等)
  - 成语相关schemas(ChengyuCreate, ChengyuResponse等)
  - 词语相关schemas(CiyuCreate, CiyuResponse等)
  - 通用响应schemas(APIResponse, PaginatedResponse等)

### 5. `test_simple_api.py` - ORM数据库查询测试
- **用途**: 测试数据库模型的实际查询功能
- **适用场景**: 
  - 验证数据库操作正确性
  - 数据查询功能测试
  - 性能初步评估
- **测试内容**:
  - 成语总数查询
  - 包含特定字的成语搜索
  - 常用词语查询
  - 汉字数据查询

### 6. `test_fastapi_endpoints.py` - FastAPI端点测试
- **用途**: 测试所有FastAPI接口端点的完整功能
- **适用场景**: 
  - 完整API功能验证
  - 回归测试
  - 集成测试
- **测试内容**:
  - 用户认证（管理员、老师）
  - 健康检查端点
  - 用户信息获取
  - 成语管理（列表、搜索、详情、创建）
  - 词语管理（列表、搜索、详情、创建）
  - 权限控制测试
  - 错误情况处理

## 🚀 测试运行指南

### 基础设施测试
```bash
# 测试数据库连接和数据
cd backend
uv run python tests/test_db_connection.py

# 查看数据库表结构
uv run python tests/check_table_structure.py

# 测试SQLAlchemy模型
uv run python tests/test_models.py

# 测试数据模式
uv run python tests/test_schemas.py
```

### ORM功能测试
```bash
cd backend
uv run python tests/test_simple_api.py
```

### API端点测试
```bash
# 确保FastAPI服务在运行
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 在新终端运行测试
uv run python tests/test_fastapi_endpoints.py
```

### 运行所有测试
```bash
# 顺序运行所有测试（推荐）
cd backend
uv run python tests/test_db_connection.py
uv run python tests/test_models.py
uv run python tests/test_schemas.py
uv run python tests/test_simple_api.py
# 然后启动API服务器
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# 在新终端
uv run python tests/test_fastapi_endpoints.py
```

## 🧪 测试期望结果

### 数据库连接测试
- **✅ 连接成功**: 能够连接到数据库
- **✅ 表列表**: 显示所有相关数据表
- **✅ 记录统计**: 各表记录数正确显示
- **✅ 查询验证**: 基本SQL查询正常执行

### 模型测试
- **✅ 模型映射**: 所有SQLAlchemy模型正确映射到数据库表
- **✅ 字段匹配**: 模型字段与数据库字段一一对应
- **✅ 关系验证**: 外键关系正确建立

### 模式测试
- **✅ 数据验证**: 输入数据按照模式规则验证
- **✅ 序列化**: 数据正确序列化为JSON格式
- **✅ 反序列化**: JSON正确转换为Python对象

### ORM查询测试
- **✅ 成语查询**: 成语总数和搜索功能正常
- **✅ 词语查询**: 词语搜索和列表获取正常
- **✅ 汉字查询**: 汉字数据查询正常

### API端点测试
#### 认证功能
- **✅ 管理员登录** (`admin/admin123`)
- **✅ 老师登录** (`teacher/teach123`)
- **✅ 错误登录拒绝**
- **✅ 无效token拒绝**
- **✅ 无认证访问拒绝**

#### 成语管理
- **✅ 获取成语列表**（分页）
- **✅ 成语搜索功能**
- **✅ 获取单个成语详情**
- **✅ 创建新成语**（管理员/老师）
- **✅ 权限检查**

#### 词语管理
- **✅ 获取词语列表**（分页）
- **✅ 词语搜索功能**
- **✅ 获取单个词语详情**
- **⚠️ 创建新词语**（待修复）

#### 权限系统
- **✅ 管理员完全访问**
- **✅ 老师读/写访问**
- **✅ 未认证用户拒绝**
- **✅ 无效权限拒绝**

## 📊 数据验证标准

### 数据量预期
- **成语总数**: ~46,360条
- **词语总数**: ~217,430条
- **搜索结果**: 包含搜索词的相关记录
- **分页**: 默认每页20条

### API状态码验证
- `200` - 成功响应
- `401` - 未认证/无效token
- `403` - 权限不足
- `404` - 资源不存在
- `409` - 资源重复
- `500` - 服务器内部错误

## 🔧 故障排除

### 数据库测试问题
1. **连接失败**: 检查数据库配置和连接参数
2. **表不存在**: 确保数据库已创建并包含必要表结构
3. **权限问题**: 确保数据库用户有足够权限查询表

### 模型和模式测试问题
1. **模型映射错误**: 检查模型定义与实际表结构是否匹配
2. **模式验证失败**: 确认Pydantic模式定义正确
3. **导入错误**: 检查Python路径和模块导入

### API端点测试问题
1. **连接拒绝**: 确保FastAPI服务在8000端口运行
2. **认证失败**: 检查用户名和密码正确性
3. **数据验证错误**: 检查请求JSON格式和必填字段
4. **权限错误**: 确保使用正确的用户角色登录

### 调试技巧
1. **查看详细错误信息**: 测试失败时查看完整错误堆栈
2. **分步测试**: 从最基础的连接测试开始，逐步向上级测试
3. **检查服务器日志**: 查看FastAPI服务器的控制台日志
4. **手动测试**: 使用 `http://localhost:8000/docs` 手动测试API
5. **网络检查:** 使用网络工具检查API端点可达性

## 📝 测试扩展

### 添加新测试文件
1. 在tests目录创建新测试文件
2. 遵循现有文件命名模式(如`test_功能.py`)
3. 包含标准文档字符串和注释
4. 使用一致的输出格式（✅/❌）

### 添加新测试用例
1. 在对应测试文件中添加新方法
2. 包含适当的异常处理
3. 添加详细的测试描述
4. 验证边界条件和异常情况

### 创建测试数据
- 使用测试专用数据库避免污染生产数据
- 创建可重复的测试数据集
- 实现测试后的数据清理

## 🎯 测试最佳实践

1. **分层测试**: 从基础连接到业务逻辑逐层测试
2. **独立性**: 每个测试应该可以独立运行
3. **全面覆盖**: 测试正常流程、异常情况、边界条件
4. **清晰反馈**: 使用 ✅ 和 ❌ 等标记提供明确结果
5. **异常处理**: 捕获并适当处理各种异常
6. **性能考虑**: 注意大数据量查询的性能影响
7. **安全测试**: 验证权限控制和输入安全

## 📈 测试自动化

### 批量执行脚本
创建批量测试脚本便于执行所有测试：

```bash
#!/bin/bash
# 运行所有测试的脚本
echo "开始运行全部测试..."

echo "1. 测试数据库连接..."
uv run python tests/test_db_connection.py

echo "2. 检查表结构..."
uv run python tests/check_table_structure.py

echo "3. 测试SQLAlchemy模型..."
uv run python tests/test_models.py

echo "4. 测试数据模式..."
uv run python tests/test_schemas.py

echo "5. 测试ORM查询..."
uv run python tests/test_simple_api.py

echo "启动API服务器进行端点测试..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 &
sleep 10

echo "6. 测试API端点..."
uv run python tests/test_fastapi_endpoints.py

echo "所有测试完成！"
```

### CI/CD集成
在持续集成流水线中运行测试：

```yaml
# GitHub Actions 示例
- name: Setup Python
  uses: actions/setup-python@v2
  with:
    python-version: '3.11'

- name: Install dependencies
  run: |
    cd backend
    pip install -r requirements.txt

- name: Run Database Tests
  run: |
    cd backend
    python tests/test_db_connection.py
    python tests/test_models.py

- name: Start API Server
  run: |
    cd backend
    uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    sleep 10

- name: Run API Tests
  run: |
    cd backend
    python tests/test_fastapi_endpoints.py
```

这样可以确保每次代码变更后系统功能仍然正常工作，提高代码质量和可靠性。