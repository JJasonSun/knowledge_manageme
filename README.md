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

3. 激活虚拟环境并启动后端服务：
   ```bash
   # 方式一：使用 uv run（推荐）
   uv run uvicorn app.main:app --reload --port 8000
   
   # 方式二：激活虚拟环境后运行
   # Windows:
   .venv\Scripts\activate
   uvicorn app.main:app --reload --port 8000
   
   # Linux/macOS:
   source .venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

   **重要提示**：
   - 确保在 `backend` 目录下运行命令
   - 如果遇到 "program not found" 错误，请确保已正确安装 uv 并且在正确的目录下
   - 首次运行会自动根据 `app/core/database.py` 中的逻辑初始化数据库表结构

4. 验证后端启动成功：
   - 访问 http://localhost:8000/docs 查看 API 文档
   - 访问 http://localhost:8000/health 检查服务状态

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

### 模块架构
系统已重构为三大核心模块，采用模块化设计：

#### 1️⃣ 汉字模块
- **字**：汉字管理（框架已搭建，待后端实现）
- **词**：词语管理（支持增删改查，包含拼音、释义、例句等字段）
- **成语**：成语管理（支持增删改查，包含拼音、释义、例句、出处等字段）

#### 2️⃣ 题目模块
- **HSK考试**：听力题、阅读题、书写题、写作题
- **YCT考试**：听力题、阅读题、书写题、写作题
- *注：框架已搭建，待后端实现数据*

#### 3️⃣ 音视频资源模块
- **音频资源**：音频资源管理（框架已搭建，待后端实现）
- **视频资源**：视频资源管理（框架已搭建，待后端实现）

### 系统特性

- **权限管理**:
  - **管理员 (Admin)**: 拥有最高权限，可以查看、编辑和删除系统中所有的成语和词语资源。
  - **老师 (Teacher)**: 可以创建自己的资源，但只能查看、编辑和删除自己创建的内容。
- **智能搜索**: 首页支持二级级联搜索，先选择模块再选择子类型，支持模糊搜索。
- **模块导航**: 顶部导航栏采用下拉菜单形式，各模块下显示子选项，方便快速访问。
- **响应式设计**: 前端采用 Vue 3 开发，提供流畅的用户交互体验。
 - **统一UI**: 采用清爽绿色主题（#66bb6a 主色），模块按钮/搜索区一致的圆角与阴影。

## 前端路由结构

```
/home                          - 首页（级联搜索 + 模块展示）
/hanzi/zi                     - 汉字管理
/hanzi/ciyu                   - 词语管理
/hanzi/chengyu                - 成语管理
/exam/hsk/listening           - HSK听力题
/exam/hsk/reading             - HSK阅读题
/exam/hsk/writing             - HSK书写题
/exam/hsk/essay               - HSK写作题
/exam/yct/listening           - YCT听力题
/exam/yct/reading             - YCT阅读题
/exam/yct/writing             - YCT书写题
/exam/yct/essay               - YCT写作题
/media/audio                   - 音频资源
/media/video                   - 视频资源
```

**路由重定向**：
- `/chengyu` → `/hanzi/chengyu`（向后兼容）
- `/ciyu` → `/hanzi/ciyu`（向后兼容）

## 项目结构更新

### 前端目录结构
```
frontend/
├── src/
│   ├── components/
│   │   └── Header.vue              # 更新：添加三个模块下拉菜单
│   ├── router/
│   │   └── index.js                # 更新：新增13个路由
│   ├── stores/
│   │   └── auth.js                 # 认证状态管理
│   ├── utils/
│   │   └── request.js              # HTTP请求封装
│   └── views/
│       ├── Home.vue                # 更新：级联搜索 + 模块卡片
│       ├── CiyuList.vue            # 词语管理列表
│       ├── ChengyuList.vue         # 成语管理列表
│       ├── hanzi/
│       │   └── HanziList.vue       # 新增：汉字管理
│       ├── exam/
│       │   ├── ExamTemplate.vue    # 新增：题目通用模板
│       │   ├── HSKListening.vue    # 新增
│       │   ├── HSKReading.vue      # 新增
│       │   ├── HSKWriting.vue      # 新增
│       │   ├── HSKEssay.vue        # 新增
│       │   ├── YCTListening.vue    # 新增
│       │   ├── YCTReading.vue      # 新增
│       │   ├── YCTWriting.vue      # 新增
│       │   └── YCTEssay.vue        # 新增
│       └── media/
│           ├── AudioList.vue       # 新增：音频资源
│           └── VideoList.vue       # 新增：视频资源
```

## 最近前端改进（UI/交互）

- 顶部导航下拉指示改为折线型，悬停自动翻转，去掉倒三角。
- 首页搜索区：二级级联选择 + 按钮/回车触发搜索，改为绿主题胶囊风格，大卡片背景与渐变点缀。
- 列表页：创建者/常用程度标签统一为无边框圆角徽章，系统灰、其他淡黄，常用绿、非常用深灰；占位卡片去掉虚线边框。
- 资源列表搜索：成语/词语列表改为显式点击或回车触发，取消实时输入自动搜索。
- 模块卡片按钮：柔和渐变、细边与轻阴影，悬停微抬升，图标块统一样式。
- **操作按钮**：列表页操作列显示三个按钮（查看/编辑/删除），编辑和删除按钮根据权限动态显示。
- **详情弹窗**：点击"查看"按钮弹出详情弹窗，样式与首页搜索结果弹窗一致，显示完整字段信息。
- **权限控制**：管理员可编辑/删除所有资源，老师只能编辑/删除自己创建的资源。

## 常见问题

### 后端启动问题

1. **错误**: `Failed to spawn: uvicorn` 或 `program not found`
   - **解决方案**: 确保在 `backend` 目录下运行命令，并且已正确安装依赖
   ```bash
   cd backend
   uv sync  # 重新同步依赖
   uv run uvicorn app.main:app --reload --port 8000
   ```

2. **错误**: 数据库连接失败
   - **解决方案**: 检查 `backend/.env` 文件中的数据库配置
   - 确保 MySQL 服务正在运行

3. **错误**: 端口被占用
   - **解决方案**: 更换端口或停止占用端口的进程
   ```bash
   uv run uvicorn app.main:app --reload --port 8001  # 使用其他端口
   ```

### 前端启动问题

1. **错误**: `npm install` 失败
   - **解决方案**: 清除缓存后重新安装
   ```bash
   npm cache clean --force
   npm install
   ```

2. **错误**: API 请求失败
   - **解决方案**: 确保后端服务已启动并运行在正确端口
   - 检查 `frontend/vite.config.js` 中的代理配置

## 测试账号

- **管理员**: `admin` / `admin123` （可管理所有资源）
- **老师**: `teacher` / `teach123` （只能管理自己创建的资源）
