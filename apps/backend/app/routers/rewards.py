"""
Rewards Router
Handles points system and leaderboard
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


@router.get("/points")
async def get_my_points(db: Session = Depends(get_db)):
    """
    Get current user's reward points
    """
    return {"message": "Get points - to be implemented"}


@router.get("/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    """
    Get facility leaderboard
    """
    return {"message": "Get leaderboard - to be implemented"}


@router.get("/history")
async def get_points_history(db: Session = Depends(get_db)):
    """
    Get user's points earning history
    """
    return {"message": "Get points history - to be implemented"}
