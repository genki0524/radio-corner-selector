"""
番組のCRUD操作
Repository実装の後方互換ラッパー
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Program
from cruds.program_repository_impl import ProgramRepositoryImpl


def get_programs(
    db: Session,
    user_id: int,
    personality_id: Optional[int] = None,
    search: Optional[str] = None
) -> List[Program]:
    """番組一覧を取得（パーソナリティや番組名での絞り込み可能）"""
    repo = ProgramRepositoryImpl(db)
    return repo.get_by_user_id(user_id, personality_id, search)


def get_program(db: Session, program_id: int) -> Optional[Program]:
    """番組を取得"""
    repo = ProgramRepositoryImpl(db)
    return repo.get_by_id(program_id)


def create_program(
    db: Session,
    program_data: dict,
    personality_ids: Optional[List[int]] = None,
    corners_data: Optional[List[dict]] = None
) -> Program:
    """番組を作成"""
    repo = ProgramRepositoryImpl(db)
    return repo.create_from_dict(program_data, personality_ids or [], corners_data)


def update_program(
    db: Session,
    program_id: int,
    program_data: dict,
    personality_ids: Optional[List[int]] = None
) -> Optional[Program]:
    """番組を更新"""
    repo = ProgramRepositoryImpl(db)
    return repo.update_from_dict(program_id, program_data, personality_ids)


def delete_program(db: Session, program_id: int) -> bool:
    """番組を削除"""
    repo = ProgramRepositoryImpl(db)
    return repo.delete(program_id)