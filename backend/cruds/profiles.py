"""
プロフィールのCRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Profile


def get_profiles(db: Session, user_id: int) -> List[Profile]:
    """プロフィール一覧を取得"""
    return db.query(Profile).filter(Profile.user_id == user_id).all()


def get_profile(db: Session, profile_id: int) -> Optional[Profile]:
    """プロフィールを取得"""
    return db.query(Profile).filter(Profile.id == profile_id).first()


def create_profile(db: Session, profile_data: dict) -> Profile:
    """プロフィールを作成"""
    db_profile = Profile(**profile_data)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, profile_id: int, profile_data: dict) -> Optional[Profile]:
    """プロフィールを更新"""
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        return None
    
    for key, value in profile_data.items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, profile_id: int) -> bool:
    """プロフィールを削除"""
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        return False
    
    db.delete(db_profile)
    db.commit()
    return True
