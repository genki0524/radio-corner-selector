"""
プロフィールサービス
ビジネスロジックを集約
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from cruds import profiles as profile_crud
from schemas import ProfileCreate, ProfileUpdate, ProfileResponse


def get_profiles(db: Session, user_id: int) -> List[ProfileResponse]:
    """プロフィール一覧を取得"""
    return profile_crud.get_profiles(db, user_id)


def get_profile(db: Session, profile_id: int) -> Optional[ProfileResponse]:
    """プロフィールを取得"""
    return profile_crud.get_profile(db, profile_id)


def create_profile(db: Session, profile: ProfileCreate) -> ProfileResponse:
    """プロフィールを作成"""
    return profile_crud.create_profile(db, profile.model_dump())


def update_profile(
    db: Session,
    profile_id: int,
    profile: ProfileUpdate
) -> Optional[ProfileResponse]:
    """プロフィールを更新"""
    return profile_crud.update_profile(db, profile_id, profile.model_dump(exclude_unset=True))


def delete_profile(db: Session, profile_id: int) -> bool:
    """プロフィールを削除"""
    return profile_crud.delete_profile(db, profile_id)
