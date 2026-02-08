from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from ..core.database import get_db
from ..models import User, Folder
from ..schemas import FolderCreate, FolderResponse, FolderListResponse
from .auth import get_current_user

router = APIRouter(prefix="/api/folders", tags=["文件夹"])


@router.post("", response_model=FolderResponse)
async def create_folder(
    folder: FolderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建文件夹"""
    # 检查父文件夹是否存在
    if folder.parent_id:
        parent_folder = db.query(Folder).filter(
            Folder.id == folder.parent_id,
            Folder.user_id == current_user.id
        ).first()
        if not parent_folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="父文件夹不存在"
            )

    # 检查同名文件夹
    existing_folder = db.query(Folder).filter(
        Folder.user_id == current_user.id,
        Folder.name == folder.name,
        Folder.parent_id == folder.parent_id
    ).first()

    if existing_folder:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件夹名称已存在"
        )

    # 创建文件夹
    new_folder = Folder(
        user_id=current_user.id,
        name=folder.name,
        parent_id=folder.parent_id
    )
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)

    return new_folder


@router.get("", response_model=FolderListResponse)
async def get_folders(
    parent_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文件夹列表"""
    query = db.query(Folder).filter(Folder.user_id == current_user.id)

    if parent_id is not None:
        query = query.filter(Folder.parent_id == parent_id)
    else:
        query = query.filter(Folder.parent_id.is_(None))

    folders = query.order_by(Folder.created_at.desc()).all()

    return FolderListResponse(folders=folders)


@router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder(
    folder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文件夹信息"""
    folder = db.query(Folder).filter(
        Folder.id == folder_id,
        Folder.user_id == current_user.id
    ).first()

    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件夹不存在"
        )

    return folder


@router.delete("/{folder_id}")
async def delete_folder(
    folder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文件夹"""
    folder = db.query(Folder).filter(
        Folder.id == folder_id,
        Folder.user_id == current_user.id
    ).first()

    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件夹不存在"
        )

    # 删除文件夹及其子文件夹和文件
    db.delete(folder)
    db.commit()

    return {"message": "文件夹已删除"}
