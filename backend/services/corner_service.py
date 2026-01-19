"""
コーナーサービス
ビジネスロジックを集約
Repository Interfaceを使用
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from cruds.corner_repository_impl import CornerRepositoryImpl
from domain.repositories.corner_repository import CornerRepositoryInterface
from schemas import CornerCreate, CornerUpdate, CornerResponse


def _get_repository(db: Session) -> CornerRepositoryInterface:
    """Repositoryインスタンスを取得（DI用）"""
    return CornerRepositoryImpl(db)


def get_corners(db: Session, program_id: int) -> List[CornerResponse]:
    """コーナー一覧を取得"""
    repo = _get_repository(db)
    return repo.get_by_program_id(program_id)


def get_corner(db: Session, corner_id: int) -> Optional[CornerResponse]:
    """コーナーを取得"""
    repo = _get_repository(db)
    return repo.get_by_id(corner_id)


def create_corner(db: Session, corner: CornerCreate) -> CornerResponse:
    """コーナーを作成"""
    repo = _get_repository(db)
    return repo.create_from_dict(corner.model_dump())


def update_corner(
    db: Session,
    corner_id: int,
    corner: CornerUpdate
) -> Optional[CornerResponse]:
    """コーナーを更新"""
    repo = _get_repository(db)
    return repo.update_from_dict(corner_id, corner.model_dump(exclude_unset=True))


def delete_corner(db: Session, corner_id: int) -> bool:
    """コーナーを削除"""
    repo = _get_repository(db)
    return repo.delete(corner_id)
