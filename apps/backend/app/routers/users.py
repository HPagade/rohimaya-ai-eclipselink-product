"""
Users Router
Handles user profile management
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


@router.get("/profile")
async def get_profile(db: Session = Depends(get_db)):
    """
    Get current user's profile
    """
    return {"message": "Get profile - to be implemented"}


@router.put("/profile")
async def update_profile(db: Session = Depends(get_db)):
    """
    Update current user's profile
    """
    return {"message": "Update profile - to be implemented"}


@router.post("/change-password")
async def change_password(db: Session = Depends(get_db)):
    """
    Change user password
    """
    return {"message": "Change password - to be implemented"}


@router.get("/")
async def get_users(db: Session = Depends(get_db)):
    """
    Get all users in facility (admin only)
    """
    return {"message": "Get users - to be implemented"}
