from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import User
from ..schemas import StorageInfo
from .auth import get_current_user

router = APIRouter(prefix="/api/storage", tags=["存储"])


@router.get("", response_model=StorageInfo)
async def get_storage_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取存储空间信息"""
    storage_available = current_user.storage_limit - current_user.storage_used
    usage_percentage = (current_user.storage_used / current_user.storage_limit) * 100

    return StorageInfo(
        storage_used=current_user.storage_used,
        storage_limit=current_user.storage_limit,
        storage_available=storage_available,
        usage_percentage=round(usage_percentage, 2)
    )
