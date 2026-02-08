import os
import uuid
import aiofiles
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from ..models import User, File, Folder
from ..core.config import settings


class FileService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def get_user_dir(self, user_id: int) -> Path:
        """获取用户上传目录"""
        user_dir = self.upload_dir / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    async def save_file(self, file: UploadFile, user_id: int, folder_id: Optional[int] = None) -> File:
        """保存文件"""
        # 生成唯一文件名
        file_ext = os.path.splitext(file.filename)[1]
        stored_name = f"{uuid.uuid4().hex}{file_ext}"

        # 保存文件
        user_dir = self.get_user_dir(user_id)
        file_path = user_dir / stored_name

        try:
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

        return stored_name, str(file_path)

    async def delete_file(self, file_path: str):
        """删除物理文件"""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
        except Exception as e:
            print(f"删除文件失败: {e}")

    def check_storage_limit(self, user: User, file_size: int) -> bool:
        """检查存储空间限制"""
        if user.storage_used + file_size > user.storage_limit:
            return False
        return True

    def update_user_storage(self, db: Session, user: User, file_size: int, is_delete: bool = False):
        """更新用户存储空间使用量"""
        if is_delete:
            user.storage_used = max(0, user.storage_used - file_size)
        else:
            user.storage_used += file_size
        db.commit()


file_service = FileService()
