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
- ✅ **大文件上传**（单文件最大 10GB）
- ✅ 文件上传（支持拖拽点击）
- ✅ 文件下载（单个/批量打包）
- ✅ **文件管理**（查看历史上传记录、搜索文件）
- ✅ 文件删除（单个/批量）
- ✅ 存储空间管理（实时显示使用情况）
- ✅ 响应式设计（支持手机/平板/电脑）
- ✅ 10GB 存储空间

## 配置说明

### SMTP 邮件服务配置

要启用真实的邮件验证码发送功能，需要配置 SMTP 服务。推荐使用 Gmail：

#### 1. Gmail 配置步骤

1. **开启两步验证**
   - 访问 https://myaccount.google.com/security
   - 找到"两步验证"并开启

2. **生成应用专用密码**
   - 访问 https://myaccount.google.com/apppasswords
   - 选择"邮件"和"其他（自定义名称）"
   - 生成密码（例如：`abcd efgh ijkl mnop`）

3. **修改 docker-compose.yml**
   ```yaml
   services:
     backend:
       environment:
         - SMTP_HOST=smtp.gmail.com
         - SMTP_PORT=587
         - SMTP_USER=your-email@gmail.com
         - SMTP_PASSWORD=your-app-password  # 应用专用密码（注意空格）
         - SMTP_FROM=your-email@gmail.com
   ```

4. **重启容器**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

#### 其他邮箱服务

**QQ 邮箱**
```yaml
- SMTP_HOST=smtp.qq.com
- SMTP_PORT=587
- SMTP_USER=your@qq.com
- SMTP_PASSWORD=your-authorization-code
```

**163 邮箱**
```yaml
- SMTP_HOST=smtp.163.com
- SMTP_PORT=465
- SMTP_USER=your@163.com
- SMTP_PASSWORD=your-authorization-code
```

**开发模式**
- 如果不配置 SMTP（保持为空），验证码将打印到后端日志中
- 查看日志：`docker logs quicktransfer-backend`

### 其他配置

复制 `backend/.env.example` 为 `backend/.env` 并修改配置：

```env
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite+aiosqlite:///./quicktransfer.db
```

## 许可证

MIT

