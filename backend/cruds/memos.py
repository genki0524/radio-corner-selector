"""
メモのCRUD操作
Repository実装の後方互換ラッパー
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Memo
from cruds.memo_repository_impl import MemoRepositoryImpl


def get_memos(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Memo]:
    """メモ一覧を取得"""
    repo = MemoRepositoryImpl(db)
    return repo.get_by_user_id(user_id, skip, limit)


def get_memo(db: Session, memo_id: int) -> Optional[Memo]:
    """メモを取得"""
    repo = MemoRepositoryImpl(db)
    return repo.get_by_id(memo_id)


def create_memo(db: Session, memo_data: dict) -> Memo:
    """メモを作成"""
    repo = MemoRepositoryImpl(db)
    return repo.create_from_dict(memo_data)


def update_memo(db: Session, memo_id: int, memo_data: dict) -> Optional[Memo]:
    """メモを更新"""
    repo = MemoRepositoryImpl(db)
    return repo.update_from_dict(memo_id, memo_data)


def delete_memo(db: Session, memo_id: int) -> bool:
    """メモを削除"""
    repo = MemoRepositoryImpl(db)
    return repo.delete(memo_id)
