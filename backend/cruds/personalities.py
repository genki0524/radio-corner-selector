"""
パーソナリティのCRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Personality


def get_personalities(db: Session, user_id: int) -> List[Personality]:
    """パーソナリティ一覧を取得"""
    return db.query(Personality).filter(Personality.user_id == user_id).all()


def get_personality(db: Session, personality_id: int) -> Optional[Personality]:
    """パーソナリティを取得"""
    return db.query(Personality).filter(Personality.id == personality_id).first()


def create_personality(db: Session, personality_data: dict) -> Personality:
    """パーソナリティを作成"""
    db_personality = Personality(**personality_data)
    db.add(db_personality)
    db.commit()
    db.refresh(db_personality)
    return db_personality


def update_personality(
    db: Session,
    personality_id: int,
    personality_data: dict
) -> Optional[Personality]:
    """パーソナリティを更新"""
    db_personality = db.query(Personality).filter(Personality.id == personality_id).first()
    if not db_personality:
        return None
    
    for key, value in personality_data.items():
        setattr(db_personality, key, value)
    
    db.commit()
    db.refresh(db_personality)
    return db_personality


def delete_personality(db: Session, personality_id: int) -> bool:
    """パーソナリティを削除"""
    db_personality = db.query(Personality).filter(Personality.id == personality_id).first()
    if not db_personality:
        return False
    
    db.delete(db_personality)
    db.commit()
    return True
