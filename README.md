# 快传（QuickTransfer）

> 简单快速的文件传输工具

## 技术栈

- **后端**: FastAPI + Python 3.10 + SQLite
- **前端**: Vue 3 + Vite + Tailwind CSS + Pinia
- **部署**: Docker + Nginx

## 快速开始

### 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python run.py
```

### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

### Docker 部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 功能特性

- ✅ 邮箱验证码登录
- ✅ 文件上传（支持拖拽）
- ✅ 文件下载（单个/批量）
- ✅ 文件夹管理
- ✅ 在线预览（图片、PDF、视频等）
- ✅ 存储空间管理
- ✅ 10GB 存储空间

## 配置说明

复制 `backend/.env.example` 为 `backend/.env` 并修改配置：

```env
SECRET_KEY=your-secret-key
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 许可证

MIT
