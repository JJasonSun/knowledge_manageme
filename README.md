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
   uv run uvicorn app.main:app --reload --port 8003

   # 方式二：激活虚拟环境后运行
   # Windows:
   .venv\Scripts\activate
   uvicorn app.main:app --reload --port 8003

   # Linux/macOS:
   source .venv/bin/activate
   uvicorn app.main:app --reload --port 8003
   ```

   **重要提示**：

   - 确保在 `backend` 目录下运行命令
   - 如果遇到 "program not found" 错误，请确保已正确安装 uv 并且在正确的目录下
   - 首次运行会自动根据 `app/core/database.py` 中的逻辑初始化数据库表结构
4. 验证后端启动成功：

   - 访问 http://localhost:8003/docs 查看 API 文档
   - 访问 http://localhost:8003/health 检查服务状态

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

   *前端默认代理配置会指向 `http://localhost:8003/api`。*
4. (可选) 生产环境构建：

   ```bash
   npm run build
   ```

## 核心功能

### 模块架构

系统已重构为三大核心模块，采用模块化设计：

#### 1️⃣ 基础知识模块

- **字**：汉字管理（支持增删改查，包含 Unicode、URL、JSON 格式的基本信息与释义信息）
- **词**：词语管理（支持增删改查，包含拼音、释义、例句等字段）
- **成语**：成语管理（支持增删改查，包含拼音、释义、例句、出处等字段）

#### 2️⃣ 题目模块

基于数据库结构文档重构，分为两个独立系统：

- **Content System（基础课程体系）**：

  - 支持听、说、读、写四大技能分类
  - 多种题型：听音选图、听音判断、朗读句子、阅读理解、填空题等
  - 题目与单词关联，支持 HSK 等级标注
  - 媒体资源管理（音频、视频、图片）
  - 质检状态管理（待审、已通过、已驳回）
  - 权限控制：只能编辑/删除自己创建的题目
- **Scenario System（AI 情境学习）**：

  - AI 动态生成题目和课程内容
  - 支持对话和文章两种课程类型
  - 基于生成课程自动产出练习题
  - 词汇包管理，关联课程与词汇
  - 完整的生成任务追踪
  - 支持题目重新生成

**展示特色**：

- 📊 卡片式布局，信息丰富直观
- 🔗 完整展示关联数据（单词、课程、媒体、词汇）
- 🎨 多维度筛选（技能分类、题型、难度、质检状态）
- 📈 统计面板（题目总数、各技能分布）
- 🤖 AI 生成标识和课程内容预览

*注：当前使用 Mock 数据进行前端开发，待数据库配置完成后接入真实 API*

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
/exam/content-system          - Content System 题目管理
/exam/scenario-system         - Scenario System AI生成题目
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
│   │   └── Header.vue              # 更新：题目模块菜单简化
│   ├── mock/
│   ├── router/
│   │   └── index.js                # 更新：题目路由重构
│   ├── stores/
│   │   └── auth.js                 # 认证状态管理
│   ├── utils/
│   │   └── request.js              # HTTP请求封装
│   └── views/
│       ├── Home.vue                # 更新：级联搜索 + 模块卡片
│       ├── CiyuList.vue            # 词语管理列表
│       ├── ChengyuList.vue         # 成语管理列表
│       ├── hanzi/
│       │   └── HanziList.vue       # 汉字管理
│       ├── exam/
│       │   ├── ContentSystemExercises.vue    # 新增：Content System 题目管理
│       │   └── ScenarioSystemExercises.vue   # 新增：Scenario System AI题目
│       └── media/
│           ├── AudioList.vue       # 音频资源
│           └── VideoList.vue       # 视频资源
```

## 最近前端改进（UI/交互）

### 基础知识模块重构（2026-01）

- **架构统一**：将汉字、词语、成语统一为“基础知识”模块
- **路由重构**：所有基础知识相关路由统一使用 `/basic/` 前缀
- **文件组织**：相关视图文件统一移动至 `frontend/src/views/basic/` 目录

### 题目模块重构（2026-01）

- **架构调整**：删除旧的 HSK/YCT 分类，基于数据库结构文档重构为 Content System 和 Scenario System
- **数据集成**：前端已对接真实后端 API，移除 Mock 数据
- **卡片式展示**：
  - Content System：展示题目、关联单词、媒体资源、题目详情（选项、答案、解析）
  - Scenario System：展示 AI 生成题目、来源课程、考察词汇、课程内容预览
- **丰富的筛选功能**：技能分类、题型、难度、质检状态、来源课程等多维度筛选
- **统计面板**：题目总数、各技能分布、生成课程数、词汇库数量
- **关联数据展示**：完整展示单词信息、媒体资源、课程内容、词汇详情
- **权限控制**：Content System 支持创建者权限判断，只能编辑/删除自己的题目

### 通用改进（2025-12）

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
   uv run uvicorn app.main:app --reload --port 8003
   ```
2. **错误**: 数据库连接失败

   - **解决方案**: 检查 `backend/.env` 文件中的数据库配置
   - 确保 MySQL 服务正在运行
3. **错误**: 端口被占用

   - **解决方案**: 更换端口或停止占用端口的进程

   ```bash
   uv run uvicorn app.main:app --reload --port 8004  # 使用其他端口
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

- **管理员**: `admin` / `123456` （可管理所有资源）
- **老师1**: `teacher1` / `123456` （只能管理自己创建的资源）
- **老师2**: `teacher2` / `123456` （只能管理自己创建的资源）
