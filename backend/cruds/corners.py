"""
コーナーのCRUD操作
Repository実装の後方互換ラッパー
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Corner
from cruds.corner_repository_impl import CornerRepositoryImpl


def get_corners(db: Session, program_id: int) -> List[Corner]:
    """コーナー一覧を取得"""
    repo = CornerRepositoryImpl(db)
    return repo.get_by_program_id(program_id)


def get_corner(db: Session, corner_id: int) -> Optional[Corner]:
    """コーナーを取得"""
    repo = CornerRepositoryImpl(db)
    return repo.get_by_id(corner_id)


def create_corner(db: Session, corner_data: dict) -> Corner:
    """コーナーを作成"""
    repo = CornerRepositoryImpl(db)
    return repo.create_from_dict(corner_data)


def update_corner(db: Session, corner_id: int, corner_data: dict) -> Optional[Corner]:
    """コーナーを更新"""
    repo = CornerRepositoryImpl(db)
    return repo.update_from_dict(corner_id, corner_data)


def delete_corner(db: Session, corner_id: int) -> bool:
    """コーナーを削除"""
    repo = CornerRepositoryImpl(db)
    return repo.delete(corner_id)