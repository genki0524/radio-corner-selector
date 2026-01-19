"""
パーソナリティ管理API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import PersonalityCreate, PersonalityUpdate, PersonalityResponse
from services import personality_service

router = APIRouter(prefix="/personalities", tags=["personalities"])


@router.get("", response_model=List[PersonalityResponse])
def get_personalities(user_id: int, db: Session = Depends(get_db)):
    """パーソナリティ一覧を取得"""
    return personality_service.get_personalities(db, user_id)


@router.get("/{personality_id}", response_model=PersonalityResponse)
def get_personality(personality_id: int, db: Session = Depends(get_db)):
    """パーソナリティを取得"""
    personality = personality_service.get_personality(db, personality_id)
    if not personality:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personality not found")
    return personality


@router.post("", response_model=PersonalityResponse, status_code=status.HTTP_201_CREATED)
def create_personality(personality: PersonalityCreate, db: Session = Depends(get_db)):
    """パーソナリティを作成"""
    return personality_service.create_personality(db, personality)


@router.put("/{personality_id}", response_model=PersonalityResponse)
def update_personality(
    personality_id: int,
    personality: PersonalityUpdate,
    db: Session = Depends(get_db)
):
    """パーソナリティを更新"""
    db_personality = personality_service.update_personality(db, personality_id, personality)
    if not db_personality:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personality not found")
    return db_personality


@router.delete("/{personality_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_personality(personality_id: int, db: Session = Depends(get_db)):
    """パーソナリティを削除"""
    if not personality_service.delete_personality(db, personality_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personality not found")
    return None
