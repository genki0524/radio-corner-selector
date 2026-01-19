"""
解析用のCRUD操作
"""
from typing import List, Tuple
from sqlalchemy.orm import Session

from models import Memo, Program, Corner


def get_memo_by_id(db: Session, memo_id: int) -> Memo:
    """メモを取得"""
    return db.query(Memo).filter(Memo.id == memo_id).first()


def get_user_corners(db: Session, user_id: int) -> List[Tuple[Corner, Program]]:
    """ユーザーの全コーナー情報を取得"""
    return (
        db.query(Corner, Program)
        .join(Program)
        .filter(Program.user_id == user_id)
        .all()
    )
