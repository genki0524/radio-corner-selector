"""
パーソナリティサービス
ビジネスロジックを集約
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from cruds import personalities as personality_crud
from schemas import PersonalityCreate, PersonalityUpdate, PersonalityResponse


def get_personalities(db: Session, user_id: int) -> List[PersonalityResponse]:
    """パーソナリティ一覧を取得"""
    return personality_crud.get_personalities(db, user_id)


def get_personality(db: Session, personality_id: int) -> Optional[PersonalityResponse]:
    """パーソナリティを取得"""
    return personality_crud.get_personality(db, personality_id)


def create_personality(db: Session, personality: PersonalityCreate) -> PersonalityResponse:
    """パーソナリティを作成"""
    return personality_crud.create_personality(db, personality.model_dump())


def update_personality(
    db: Session,
    personality_id: int,
    personality: PersonalityUpdate
) -> Optional[PersonalityResponse]:
    """パーソナリティを更新"""
    return personality_crud.update_personality(
        db, personality_id, personality.model_dump(exclude_unset=True)
    )


def delete_personality(db: Session, personality_id: int) -> bool:
    """パーソナリティを削除"""
    return personality_crud.delete_personality(db, personality_id)
