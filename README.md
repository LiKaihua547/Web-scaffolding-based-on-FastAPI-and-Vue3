Knowledge Blog — FastAPI + Vue3 全栈博客/管理系统脚手架
一个开箱即用的前后端分离全栈脚手架，包含前台展示与后台管理双布局，集成本地大模型（Ollama）对话功能。基于 FastAPI（Python）与 Vue3（组合式 API）构建，提供用户认证、自动代码生成、统一响应封装等基础能力，适合快速启动个人博客、知识库或中小型管理后台项目。

✨ 主要特性
后端
FastAPI 异步框架，自动生成 Swagger 文档

分层架构：api → services → dao → database，清晰解耦

JWT 认证：注册/登录，支持管理员角色判断

自动代码生成：根据数据库表一键生成 Pydantic 模型（model/）与 DAO 数据访问类（dao/）

统一响应格式：common/response.py 规范化输出

全局异常处理：捕获并返回友好错误信息

CORS 配置：支持前端跨域开发

MySQL / SQLite 双数据库支持（通过配置文件切换）

Ollama 本地大模型集成：提供模型列表查询、对话流式/非流式接口

前端
Vue3 + Vite：快速开发与热重载

Element Plus：UI 组件库，界面美观

双布局设计：

前台布局（FrontLayout）：顶部导航 + 可折叠侧边栏 + 右下角 AI 悬浮球

后台管理布局（AdminLayout）：深色/浅色渐变主题可选，Header 导航 + 侧边菜单 + 折叠功能

路由权限守卫：未登录自动跳转登录页，普通用户无法访问后台

Axios 请求封装：统一拦截器，处理 token 与错误

AI 助手组件：可复用的抽屉式对话界面，支持流式输出

批量页面生成脚本：Node.js 脚本一键生成 Vue 页面并输出路由配置

🛠️ 技术栈
前端	后端
Vue 3	FastAPI
Vue Router	SQLAlchemy (异步)
Element Plus	Pydantic V2
Axios	PyMySQL / aiomysql
Vite	Python-Jose (JWT)
Pinia (可选)	Passlib (密码哈希)
Ollama (本地模型)
📁 目录结构
text
knowledge-blog/
├── backend/                         # FastAPI 后端
│   ├── api/                         # 路由层（按模块拆分）
│   │   ├── user_api.py
│   │   ├── ai_api.py
│   │   └── ...
│   ├── services/                    # 业务逻辑层
│   ├── dao/                         # 数据访问层（自动生成 + 自定义）
│   ├── model/                       # Pydantic 模型（自动生成）
│   ├── database/                    # 数据库连接配置
│   ├── config/                      # 应用配置（数据库、Ollama等）
│   ├── common/                      # 公共工具（响应封装、异常处理、JWT）
│   ├── utils/                       # 辅助工具（代码生成脚本）
│   ├── main.py                      # 应用入口
│   └── requirements.txt
│
├── frontend/                        # Vue3 前端
│   ├── public/                      # 静态资源
│   ├── src/
│   │   ├── api/                     # 接口请求封装
│   │   ├── assets/                  # 图片、样式等
│   │   ├── components/              # 公共组件（AiAssistant, Layout等）
│   │   ├── views/                   # 页面视图（front/前台, admin/后台）
│   │   ├── router/                  # 路由配置
│   │   ├── utils/                   # 工具函数（request封装）
│   │   ├── scripts/                 # 页面生成脚本
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
└── README.md
### 相关图片展示
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4d38565d-d11b-4e2f-b423-e7cebf63a2d1" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4b70c1f4-5467-4f0b-9c3c-22a40addb88a" />

