# 中文教育知识管理系统 (Chinese Education Knowledge Management)

这是一个基于 FastAPI 和 Vue 3 开发的中文教育知识管理系统，主要用于成语和词语的管理与学习。系统支持多角色权限控制（管理员与老师），并提供高效的搜索和资源归属管理功能。

## 技术栈

- **后端**: FastAPI, SQLAlchemy (MySQL), JWT 认证, Pydantic
- **前端**: Vue 3 (Composition API), Vite, Pinia, Axios
- **环境管理**: [uv](https://github.com/astral-sh/uv) (高性能 Python 包管理器)

## 项目结构

```text
.
├── backend/            # FastAPI 后端代码
│   ├── app/            # 核心逻辑 (Models, Schemas, API, Core)
│   └── pyproject.toml  # 后端依赖配置
├── frontend/           # Vue 3 前端代码
│   ├── src/            # 源代码 (Views, Stores, Components)
│   └── package.json    # 前端依赖配置
└── README.md           # 项目说明文档
```

## 快速开始

### 1. 环境准备

确保已安装 `uv`。如果未安装，可以通过以下命令安装：
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 后端配置与启动

1. 进入后端目录：
   ```bash
   cd backend
   ```
2. 创建虚拟环境并安装依赖：
   ```bash
   uv venv
   uv sync
   ```
3. 启动后端服务：
   ```bash
   uv run uvicorn app.main:app --reload --port 8000
   ```
   *注意：首次运行会自动根据 `app/core/database.py` 中的逻辑初始化数据库表结构。*

### 3. 前端配置与启动

1. 进入前端目录：
   ```bash
   cd frontend
   ```
2. 安装依赖：
   ```bash
   npm install
   ```
3. 启动开发服务器：
   ```bash
   npm run dev -- --port 3001
   ```
   *前端默认代理配置会指向 `http://localhost:8000/api`。*

4. (可选) 生产环境构建：
   ```bash
   npm run build
   ```

## 核心功能

- **权限管理**:
  - **管理员 (Admin)**: 拥有最高权限，可以查看、编辑和删除系统中所有的成语和词语资源。
  - **老师 (Teacher)**: 可以创建自己的资源，但只能查看、编辑和删除自己创建的内容。
- **资源管理**: 支持成语和词语的增删改查，包含拼音、释义、例句等详细字段。
- **智能搜索**: 支持按名称、拼音或释义进行模糊搜索。
- **响应式设计**: 前端采用 Vue 3 开发，提供流畅的用户交互体验。

## 测试账号

- **管理员**: `admin` / `admin123`
- **老师**: `teacher1` / `teacher123`
