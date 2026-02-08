from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from ..core.database import get_db
from ..core.security import create_access_token
from ..models import User
from ..schemas import Token, TokenVerify, UserResponse
from ..services import email_service, verification_code_service

router = APIRouter(prefix="/api/auth", tags=["认证"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    from ..core.security import decode_access_token

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌"
        )

    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌"
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    return user


@router.post("/send-code", status_code=status.HTTP_200_OK)
async def send_verification_code(email: str):
    """发送验证码"""
    # 生成验证码
    code = verification_code_service.generate_code(email)

    # 发送邮件
    success = email_service.send_verification_code(email, code)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="验证码发送失败"
        )

    return {"message": "验证码已发送"}


@router.post("/verify-code", response_model=Token)
async def verify_code(data: TokenVerify, db: Session = Depends(get_db)):
    """验证码登录"""
    # 验证验证码
    if not verification_code_service.verify_code(data.email, data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期"
        )

    # 查找或创建用户
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        user = User(
            email=data.email,
            storage_limit=10737418240  # 10GB
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.commit()

    # 生成Token
    access_token = create_access_token(data={"sub": user.email})

    return Token(
        token=access_token,
        expires_in=2592000  # 30天
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
        last_login=current_user.last_login,
        storage_used=current_user.storage_used,
        storage_limit=current_user.storage_limit,
        storage_available=current_user.storage_limit - current_user.storage_used
    )
