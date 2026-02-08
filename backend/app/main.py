from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .core.database import engine, Base
from .api import auth_router, files_router, folders_router, storage_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="快传 API",
    description="简单快速的文件传输工具",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(files_router)
app.include_router(folders_router)
app.include_router(storage_router)

# 创建上传目录
import os
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def root():
    return {"message": "快传 API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
