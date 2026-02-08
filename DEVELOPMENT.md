# 快传（QuickTransfer）- 开发文档

## 项目概述

快传是一个浏览器即用、无文件大小限制、跨设备文件传输工具。

## 技术栈

### 后端
- **框架**: FastAPI 0.115.0
- **Python**: 3.10+
- **数据库**: SQLite
- **认证**: JWT + 邮箱验证码

### 前端
- **框架**: Vue 3
- **构建工具**: Vite
- **UI**: Tailwind CSS
- **状态管理**: Pinia
- **路由**: Vue Router

### 部署
- **容器化**: Docker + Docker Compose
- **Web服务器**: Nginx

## 项目结构

```
QuickTransfer/
├── backend/                    # 后端项目
│   ├── app/
│   │   ├── api/               # API 路由
│   │   │   ├── auth.py        # 认证接口
│   │   │   ├── files.py       # 文件接口
│   │   │   ├── folders.py     # 文件夹接口
│   │   │   └── storage.py     # 存储接口
│   │   ├── models/            # 数据库模型
│   │   ├── schemas/           # Pydantic 模型
│   │   ├── services/          # 业务逻辑
│   │   └── core/              # 核心配置
│   ├── main.py                # 应用入口
│   ├── requirements.txt       # Python 依赖
│   └── Dockerfile            # Docker 配置
│
├── frontend/                   # 前端项目
│   ├── src/
│   │   ├── api/              # API 调用
│   │   ├── components/       # 组件
│   │   ├── views/            # 页面
│   │   │   ├── Login.vue     # 登录页
│   │   │   └── Home.vue      # 主页
│   │   ├── stores/           # Pinia 状态
│   │   ├── router/           # 路由配置
│   │   └── App.vue           # 根组件
│   ├── package.json          # npm 依赖
│   ├── vite.config.js        # Vite 配置
│   └── Dockerfile           # Docker 配置
│
├── docker-compose.yml         # Docker Compose 配置
├── deploy.sh                  # 部署脚本
├── dev.sh                     # 开发启动脚本
└── README.md                  # 项目说明
```

## 功能特性

### 已实现功能 ✅

1. **用户认证**
   - 邮箱验证码登录
   - JWT Token 认证
   - 30天免登录

2. **文件管理**
   - 单文件/多文件上传
   - 拖拽上传
   - 上传进度显示
   - 文件列表展示
   - 文件搜索
   - 单文件/批量下载
   - 文件删除

3. **存储管理**
   - 存储空间显示
   - 使用率可视化
   - 10GB 存储限制

4. **跨设备同步**
   - 同一邮箱在不同设备登录看到相同文件

## 快速开始

### 开发环境

```bash
# 使用开发脚本（推荐）
./dev.sh

# 或手动启动

# 启动后端
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py

# 启动前端
cd frontend
npm install
npm run dev
```

### 生产部署

```bash
# 使用 Docker Compose
./deploy.sh

# 或手动执行
docker-compose up -d --build
```

## API 接口

### 认证接口

- `POST /api/auth/send-code` - 发送验证码
- `POST /api/auth/verify-code` - 验证码登录
- `GET /api/auth/me` - 获取当前用户信息

### 文件接口

- `POST /api/files/upload` - 上传文件
- `GET /api/files` - 获取文件列表
- `GET /api/files/{id}` - 获取文件信息
- `GET /api/files/{id}/download` - 下载文件
- `POST /api/files/batch-download` - 批量下载
- `DELETE /api/files/{id}` - 删除文件

### 文件夹接口

- `POST /api/folders` - 创建文件夹
- `GET /api/folders` - 获取文件夹列表
- `DELETE /api/folders/{id}` - 删除文件夹

### 存储接口

- `GET /api/storage` - 获取存储信息

## 配置说明

### 后端配置

编辑 `backend/.env` 文件：

```env
# 数据库
DATABASE_URL=sqlite+aiosqlite:///./quicktransfer.db

# 安全
SECRET_KEY=your-secret-key-change-this

# 邮件（可选）
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 邮件配置

如果需要真实发送邮件，配置 SMTP 参数。不配置的话，验证码会打印到后端控制台（开发模式）。

## 数据库设计

### 用户表 (users)
- id, email, created_at, last_login
- storage_used, storage_limit

### 文件表 (files)
- id, user_id, filename, stored_name
- file_path, file_size, mime_type
- folder_id, upload_time, download_count
- is_deleted

### 文件夹表 (folders)
- id, user_id, name, parent_id
- created_at

## 测试说明

### 开发环境测试

1. 启动开发服务器后，访问 http://localhost:5173
2. 输入邮箱，点击"发送验证码"
3. 查看后端控制台获取验证码
4. 输入验证码登录
5. 测试文件上传、下载、删除等功能

### API 测试

访问 http://localhost:8000/docs 查看 Swagger API 文档

## 未来优化

- [ ] 文件分片上传（支持超大文件）
- [ ] 断点续传
- [ ] WebSocket 实时通知
- [ ] 文件加密存储
- [ ] CDN 加速
- [ ] 文件分享功能
- [ ] 更丰富的文件预览

## 许可证

MIT
