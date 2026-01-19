"""
メモサービス
ビジネスロジックを集約
Repository Interfaceを使用
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from cruds.memo_repository_impl import MemoRepositoryImpl
from domain.repositories.memo_repository import MemoRepositoryInterface
from schemas import MemoCreate, MemoUpdate, MemoResponse


def _get_repository(db: Session) -> MemoRepositoryInterface:
    """Repositoryインスタンスを取得（DI用）"""
    return MemoRepositoryImpl(db)


def get_memos(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[MemoResponse]:
    """メモ一覧を取得"""
    repo = _get_repository(db)
    # 後方互換性のためORMモデルを返す
    return repo.get_by_user_id(user_id, skip, limit)


def get_memo(db: Session, memo_id: int) -> Optional[MemoResponse]:
    """メモを取得"""
    repo = _get_repository(db)
    # 後方互換性のためORMモデルを返す
    return repo.get_by_id(memo_id)


def create_memo(db: Session, memo: MemoCreate) -> MemoResponse:
    """メモを作成"""
    repo = _get_repository(db)
    return repo.create_from_dict(memo.model_dump())


def update_memo(
    db: Session,
    memo_id: int,
    memo: MemoUpdate
) -> Optional[MemoResponse]:
    """メモを更新"""
    repo = _get_repository(db)
    return repo.update_from_dict(memo_id, memo.model_dump(exclude_unset=True))


def delete_memo(db: Session, memo_id: int) -> bool:
    """メモを削除"""
    repo = _get_repository(db)
    return repo.delete(memo_id)
