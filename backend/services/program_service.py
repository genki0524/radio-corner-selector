"""
番組サービス
ビジネスロジックを集約
Repository Interfaceを使用
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from cruds.program_repository_impl import ProgramRepositoryImpl
from domain.repositories.program_repository import ProgramRepositoryInterface
from schemas import ProgramCreate, ProgramUpdate, ProgramResponse


def _get_repository(db: Session) -> ProgramRepositoryInterface:
    """Repositoryインスタンスを取得（DI用）"""
    return ProgramRepositoryImpl(db)


def get_programs(
    db: Session,
    user_id: int,
    personality_id: Optional[int] = None,
    search: Optional[str] = None
) -> List[ProgramResponse]:
    """番組一覧を取得（パーソナリティや番組名での絞り込み可能）"""
    repo = _get_repository(db)
    return repo.get_by_user_id(user_id, personality_id, search)


def get_program(db: Session, program_id: int) -> Optional[ProgramResponse]:
    """番組を取得"""
    repo = _get_repository(db)
    return repo.get_by_id(program_id)


def create_program(db: Session, program: ProgramCreate) -> ProgramResponse:
    """番組を作成"""
    program_data = program.model_dump(exclude={"personality_ids", "corners"})
    # corners_data = [c.model_dump() for c in program.corners] if program.corners else None
    
    repo = _get_repository(db)
    return repo.create_from_dict(
        program_data,
        program.personality_ids,
        # corners_data
    )


def update_program(
    db: Session,
    program_id: int,
    program: ProgramUpdate
) -> Optional[ProgramResponse]:
    """番組を更新"""
    update_data = program.model_dump(exclude={"personality_ids"}, exclude_unset=True)
    repo = _get_repository(db)
    return repo.update_from_dict(
        program_id,
        update_data,
        program.personality_ids
    )


def delete_program(db: Session, program_id: int) -> bool:
    """番組を削除"""
    repo = _get_repository(db)
    return repo.delete(program_id)
