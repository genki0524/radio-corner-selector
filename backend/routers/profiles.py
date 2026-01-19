"""
プロフィール管理API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import ProfileCreate, ProfileUpdate, ProfileResponse
from services import profile_service

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("", response_model=List[ProfileResponse])
def get_profiles(user_id: int, db: Session = Depends(get_db)):
    """プロフィール一覧を取得"""
    return profile_service.get_profiles(db, user_id)


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """プロフィールを取得"""
    profile = profile_service.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """プロフィールを作成"""
    return profile_service.create_profile(db, profile)


@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(profile_id: int, profile: ProfileUpdate, db: Session = Depends(get_db)):
    """プロフィールを更新"""
    db_profile = profile_service.update_profile(db, profile_id, profile)
    if not db_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return db_profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    """プロフィールを削除"""
    if not profile_service.delete_profile(db, profile_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return None
