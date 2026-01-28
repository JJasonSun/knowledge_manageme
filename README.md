# 中文教育知识管理系统 (Chinese Education Knowledge Management)

这是一个基于 FastAPI 和 Vue 3 开发的中文教育知识管理系统，主要用于中文教学资源的全面管理，涵盖基础知识（字、词、成语）、题目体系（Content System、Scenario System）以及音视频媒体资源。系统支持多角色权限控制（管理员与老师），并提供高度统一的 UI 交互体验。

## 🌟 核心亮点 (2026-01 最新更新)

- **高度组件化与 UI 统一性**：
  - 封装了 `PageHeader` (统一顶部导航)、`SearchBar` (标准搜索框)、`SkeletonCard` (骨架屏加载) 等核心组件。
  - 各模块采用颜色识别体系：汉字 (蓝色 🔵)、词语 (绿色 🟢)、成语 (橙色 🟠)、题目 (紫色 🟣)、媒体 (灰色 ⚪)。
- **交互体验深度优化**：
  - **搜索防抖/显式触发**：由原来的实时输入搜索改为显式点击“搜索”按钮或回车触发，极大提升了搜索稳定性，消除了输入时的页面闪烁。
  - **平滑加载**：全模块引入骨架屏 (Skeleton Screen)，在数据加载时提供更自然的过渡效果。
  - **自适应筛选**：后端驱动的动态过滤器，支持按技能分类、题型、课本、课次等多维度级联筛选。
- **后端架构升级**：
  - **多数据库支持同步优化**：同时支撑 MySQL (基础数据) 与 PostgreSQL (题目数据)，并完美适配远程 SSH 隧道连接。
  - **动态配置接口**：新增 `/filters` 端点，前端筛选项自动根据数据库内容动态生成，无需硬编码。

## 技术栈

- **后端**: FastAPI, SQLAlchemy, JWT 认证, Pydantic, SSH 隧道支持
- **前端**: Vue 3 (Composition API), Vite, Pinia, Axios, Scoped CSS
- **工具**: [uv](https://github.com/astral-sh/uv) (模块化依赖管理), Git

## 项目结构

```text
.
├── backend/            # FastAPI 后端目录
│   ├── app/
│   │   ├── api/        # 业务接口 (题目 filters, 汉字/词语/成语 CRUD)
│   │   ├── core/       # 核心配置 (Database, Auth, SSH Tunnel)
│   │   ├── models/     # 模型定义 (MySQL/PostgreSQL)
│   │   └── schemas/    # Pydantic 数据规范
│   └── pyproject.toml
├── frontend/           # Vue 3 前端目录
│   ├── src/
│   │   ├── components/ # 💡 公用组件 (Header, Search, Skeleton, FilterBar)
│   │   ├── views/      # 业务视图 (basic, exam, media)
│   │   └── stores/     # 状态管理
│   └── vite.config.js
└── README.md           # 本说明文档
```

## 核心功能模块

### 1️⃣ 基础知识模块 (Basic Knowledge)

- **汉字管理** 🔵：支持多维度属性维护。
- **词语/成语管理** 🟢🟠：包含释义、例句、同近反义词等深度教学属性。

### 2️⃣ 题目/练习模块 (Exercises)

- **Content System (基础体系)**：
  - 分类：听、说、读、写四大技能。
  - 交互：支持选项实时预览、媒体资源在线播放。
- **Scenario System (AI 情境学习)** 🟣：
  - AI 生成内容支持，包含课程原文、生成的对话及配套练习。

### 3️⃣ 媒体资源模块 (Media)

- **音视频管理**：支持系统中所有多媒体素材的分类上传与检索（持续开发中）。

## 快速开始

### 后端配置与启动 (uv 推荐)

1. 进入目录并安装依赖：

   ```bash
   cd backend
   uv sync
   ```
2. 启动服务 (默认端口 8003)：

   ```bash
   uv run uvicorn app.main:app --reload --port 8003
   ```

   *注意：系统会自动根据环境变量配置 SSH 隧道，如连接失败请检查 `database.py`。*

### 前端配置与启动

1. 进入目录并安装依赖：
   ```bash
   cd frontend
   npm install
   ```
2. 启动开发环境：
   ```bash
   npm run dev -- --port 3001
   ```

## 最近改进记录 (Changelog)

#### 🎨 UI & UX 升级

- **[新增]** 封装全量 `SkeletonCard` 组件，替代旧有的 Spinner 或空白页。
- **[新增]** `PageHeader` 组件统一了全站页面的 Emoji 标识与标题样式。
- **[优化]** 将所有搜索框统一为显式点击触发，解决 IME 输入法状态下可能导致的频繁请求问题。
- **[修复]** 修正了弹出层/下拉菜单在暗色模式下文字不可见的问题，移除了 JSON 元数据展示区冗余的滚动条。

#### ⚙️ 架构与性能

- **[重构]** 提取了 `ExerciseFilterBar` 公用筛选栏，极大减少了 `ContentSystemExercises.vue` 与 `ScenarioSystemExercises.vue` 的代码量（约 300行+）。
- **[增强]** 后端 `/api/v1/questions/filters` 接口现在能够同时从多个源表聚合 Unique 值，确保篩选项始终最新。

---

## 常见问题

### 后端启动问题

1.**错误**: `Failed to spawn: uvicorn` 或 `program not found`

- **解决方案**: 确保在 `backend` 目录下运行命令，并且已正确安装依赖

```bash
   cd backend
   uv sync  # 重新同步依赖
   uv run uvicorn app.main:app --reload --port 8003
```

2.**错误**: 数据库连接失败

- **解决方案**: 检查 `backend/.env` 文件中的数据库配置

- 确保 MySQL 服务正在运行

3.**错误**: 端口被占用

   -**解决方案**: 更换端口或停止占用端口的进程

```bash
   uv run uvicorn app.main:app --reload --port 8004  # 使用其他端口
```

### 前端启动问题

1.**错误**: `npm install` 失败

- **解决方案**: 清除缓存后重新安装

```bash
   npm cache clean --force
   npm install
```

2.**错误**: API 请求失败

- **解决方案**: 确保后端服务已启动并运行在正确端口
- 检查 `frontend/vite.config.js` 中的代理配置

## 测试账号

- **管理员**: `admin` / `123456` （可管理所有资源）

- **老师1**: `teacher1` / `123456` （只能管理自己创建的资源）

- **老师2**: `teacher2` / `123456` （只能管理自己创建的资源）
