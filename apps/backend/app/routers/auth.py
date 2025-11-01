"""
Authentication Router
Handles user registration, login, password reset, email verification
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from app.database import get_db
from app.models import User, Facility
from app.schemas import UserRegister, UserLogin, Token, UserResponse
from app.utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_active_user,
    authenticate_user
)
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    Creates facility if it doesn't exist
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Get or create facility
    facility = db.query(Facility).filter(Facility.name == user_data.facility_name).first()
    if not facility:
        facility = Facility(
            name=user_data.facility_name,
            subscription_tier="trial",
            subscription_status="active"
        )
        db.add(facility)
        db.flush()

    # Create user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        department=user_data.department,
        phone=user_data.phone,
        facility_id=facility.id,
        is_active=True,
        email_verified=True  # Skip email verification for MVP
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    access_token = create_access_token(
        data={"sub": str(new_user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Build response
    user_response = UserResponse(
        id=new_user.id,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        role=new_user.role,
        department=new_user.department,
        facility_id=new_user.facility_id,
        facility_name=facility.name,
        is_admin=new_user.is_admin,
        is_active=new_user.is_active,
        created_at=new_user.created_at
    )

    return Token(access_token=access_token, token_type="bearer", user=user_response)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login user and return JWT token
    OAuth2PasswordRequestForm uses 'username' field for email
    """
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Get facility name
    facility = db.query(Facility).filter(Facility.id == user.facility_id).first()

    # Build response
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        department=user.department,
        facility_id=user.facility_id,
        facility_name=facility.name if facility else "",
        is_admin=user.is_admin,
        is_active=user.is_active,
        created_at=user.created_at
    )

    logger.info(f"User {user.email} logged in successfully")

    return Token(access_token=access_token, token_type="bearer", user=user_response)


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout user (client should discard token)
    """
    logger.info(f"User {current_user.email} logged out")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user information
    """
    facility = db.query(Facility).filter(Facility.id == current_user.facility_id).first()

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        role=current_user.role,
        department=current_user.department,
        facility_id=current_user.facility_id,
        facility_name=facility.name if facility else "",
        is_admin=current_user.is_admin,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.post("/forgot-password")
async def forgot_password():
    """
    Send password reset email (not implemented in MVP)
    """
    return {"message": "Password reset email would be sent (not implemented in MVP)"}


@router.post("/reset-password")
async def reset_password():
    """
    Reset password with token from email (not implemented in MVP)
    """
    return {"message": "Password reset (not implemented in MVP)"}


@router.post("/verify-email")
async def verify_email():
    """
    Verify email with token (not implemented in MVP)
    """
    return {"message": "Email verification (not implemented in MVP)"}
