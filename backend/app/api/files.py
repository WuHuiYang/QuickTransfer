from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile, Query
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session
from typing import Optional
import os
import zipfile
import io
from pathlib import Path
from ..core.database import get_db
from ..models import User, File, Folder
from ..schemas import FileResponse, FileListResponse
from .auth import get_current_user
from ..services import file_service
from ..core.config import settings

router = APIRouter(prefix="/api/files", tags=["文件"])


@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    folder_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传文件"""
    # 检查文件大小
    file.file._file.seek(0, os.SEEK_END)
    file_size = file.file._file.tell()
    file.file._file.seek(0)

    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制（最大 {settings.MAX_FILE_SIZE / 1024 / 1024 / 1024}GB）"
        )

    # 检查存储空间
    if not file_service.check_storage_limit(current_user, file_size):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="存储空间不足"
        )

    # 检查文件夹是否存在
    if folder_id:
        folder = db.query(Folder).filter(
            Folder.id == folder_id,
            Folder.user_id == current_user.id
        ).first()
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件夹不存在"
            )

    # 保存文件
    stored_name, file_path = await file_service.save_file(file, current_user.id, folder_id)

    # 创建文件记录
    db_file = File(
        user_id=current_user.id,
        filename=file.filename,
        stored_name=stored_name,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type or "application/octet-stream",
        folder_id=folder_id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    # 更新用户存储空间
    file_service.update_user_storage(db, current_user, file_size)

    return db_file


@router.get("", response_model=FileListResponse)
async def get_files(
    folder_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文件列表"""
    query = db.query(File).filter(
        File.user_id == current_user.id,
        File.is_deleted == False
    )

    if folder_id is not None:
        query = query.filter(File.folder_id == folder_id)

    if search:
        query = query.filter(File.filename.contains(search))

    total = query.count()
    files = query.order_by(File.upload_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return FileListResponse(
        files=files,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文件信息"""
    file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id,
        File.is_deleted == False
    ).first()

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    return file


@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """下载文件"""
    file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id,
        File.is_deleted == False
    ).first()

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    # 更新下载次数
    file.download_count += 1
    db.commit()

    return FastAPIFileResponse(
        path=file.file_path,
        filename=file.filename,
        media_type=file.mime_type
    )


@router.post("/batch-download")
async def batch_download(
    file_ids: list[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """批量下载（打包成ZIP）"""
    if len(file_ids) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="单次打包下载文件数量不能超过100个"
        )

    files = db.query(File).filter(
        File.id.in_(file_ids),
        File.user_id == current_user.id,
        File.is_deleted == False
    ).all()

    if not files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="没有找到文件"
        )

    # 创建ZIP文件
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            if os.path.exists(file.file_path):
                zip_file.write(file.file_path, file.filename)

    zip_buffer.seek(0)

    # 更新下载次数
    for file in files:
        file.download_count += 1
    db.commit()

    from fastapi.responses import StreamingResponse

    return StreamingResponse(
        io.BytesIO(zip_buffer.read()),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=files.zip"}
    )


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文件"""
    file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id,
        File.is_deleted == False
    ).first()

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    # 软删除
    file.is_deleted = True
    db.commit()

    # 更新用户存储空间
    file_service.update_user_storage(db, current_user, file.file_size, is_delete=True)

    # 删除物理文件
    await file_service.delete_file(file.file_path)

    return {"message": "文件已删除"}
