from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    storage_used: int
    storage_limit: int
    storage_available: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    token: str
    expires_in: int


class TokenVerify(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)


class FolderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class FolderCreate(FolderBase):
    parent_id: Optional[int] = None


class FolderResponse(FolderBase):
    id: int
    user_id: int
    parent_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class FolderListResponse(BaseModel):
    folders: list[FolderResponse]


class FileBase(BaseModel):
    filename: str
    file_size: int


class FileItem(FileBase):
    id: int
    user_id: int
    stored_name: str
    file_path: str
    mime_type: str
    folder_id: Optional[int] = None
    upload_time: datetime
    download_count: int

    class Config:
        from_attributes = True


class FileListResponse(BaseModel):
    files: list[FileItem]
    total: int
    page: int
    page_size: int


class StorageInfo(BaseModel):
    storage_used: int
    storage_limit: int
    storage_available: int
    usage_percentage: float
