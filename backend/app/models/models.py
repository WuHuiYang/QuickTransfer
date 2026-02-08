from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    storage_used = Column(BigInteger, default=0)
    storage_limit = Column(BigInteger, default=10737418240)  # 10GB

    files = relationship("File", back_populates="user", cascade="all, delete-orphan")
    folders = relationship("Folder", back_populates="user", cascade="all, delete-orphan")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    stored_name = Column(String(255), unique=True, nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String(100), nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())
    download_count = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="files")
    folder = relationship("Folder", back_populates="files")


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="folders")
    files = relationship("File", back_populates="folder")
    parent = relationship("Folder", remote_side=[id])
