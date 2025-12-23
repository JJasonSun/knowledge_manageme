# 后端服务 (Backend Service)

基于 FastAPI 的中文教育知识管理系统后端服务。

## 环境要求

- Python >= 3.14
- uv (Python 包管理器)
- MySQL 数据库

## 快速启动

### 1. 安装依赖

```bash
# 创建虚拟环境
uv venv

# 安装项目依赖
uv sync

# 安装开发依赖（可选）
uv sync --group dev
```

### 2. 环境配置

创建 `.env` 文件并配置数据库连接：

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. 启动服务

```bash
# 开发模式启动（推荐）
uv run uvicorn app.main:app --reload --port 8000

# 或者激活虚拟环境后启动
# Windows:
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# Linux/macOS:
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### 4. 验证启动

- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health
- OpenAPI 规范: http://localhost:8000/openapi.json

## 项目结构

```
app/
├── api/                # API 路由
│   └── v1/            # API v1 版本
├── core/              # 核心配置
│   ├── config.py      # 应用配置
│   ├── database.py    # 数据库配置
│   ├── local_users.py # 本地用户管理
│   └── simple_auth.py # 简单认证
├── models/            # 数据模型
├── schemas/           # Pydantic 模式
├── utils/             # 工具函数
└── main.py           # 应用入口
```

## 开发工具

### 代码格式化

```bash
# 使用 black 格式化代码
uv run black .

# 使用 isort 排序导入
uv run isort .
```

### 代码检查

```bash
# 使用 flake8 检查代码质量
uv run flake8 .
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_models.py

# 运行测试并显示覆盖率
uv run pytest --cov=app
```

## 常见问题

### 1. uvicorn 命令未找到

**错误**: `Failed to spawn: uvicorn` 或 `program not found`

**解决方案**:
- 确保在 `backend` 目录下运行命令
- 重新同步依赖: `uv sync`
- 使用 `uv run` 前缀: `uv run uvicorn app.main:app --reload --port 8000`

### 2. 数据库连接失败

**解决方案**:
- 检查 `.env` 文件中的数据库配置
- 确保 MySQL 服务正在运行
- 验证数据库用户权限

### 3. 端口被占用

**解决方案**:
```bash
# 使用其他端口
uv run uvicorn app.main:app --reload --port 8001

# 或者停止占用端口的进程（Windows）
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### 4. 依赖安装失败

**解决方案**:
```bash
# 清除 uv 缓存
uv cache clean

# 重新创建虚拟环境
rm -rf .venv  # Linux/macOS
rmdir /s .venv  # Windows
uv venv
uv sync
```

## API 文档

启动服务后，访问 http://localhost:8000/docs 查看完整的 API 文档。

主要 API 端点：
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/idioms/` - 获取成语列表
- `POST /api/v1/idioms/` - 创建成语
- `GET /api/v1/words/` - 获取词语列表
- `POST /api/v1/words/` - 创建词语