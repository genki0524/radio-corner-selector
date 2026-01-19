"""
番組管理API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import ProgramCreate, ProgramUpdate, ProgramResponse
from services import program_service

router = APIRouter(prefix="/programs", tags=["programs"])


@router.get("", response_model=List[ProgramResponse])
def get_programs(
    user_id: int,
    personality_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """番組一覧を取得（パーソナリティや番組名での絞り込み可能）"""
    return program_service.get_programs(db, user_id, personality_id, search)


@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(program_id: int, db: Session = Depends(get_db)):
    """番組を取得"""
    program = program_service.get_program(db, program_id)
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Program not found")
    return program


@router.post("", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED)
def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    """番組を作成"""
    return program_service.create_program(db, program)


@router.put("/{program_id}", response_model=ProgramResponse)
def update_program(program_id: int, program: ProgramUpdate, db: Session = Depends(get_db)):
    """番組を更新"""
    db_program = program_service.update_program(db, program_id, program)
    if not db_program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Program not found")
    return db_program


@router.delete("/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program(program_id: int, db: Session = Depends(get_db)):
    """番組を削除"""
    if not program_service.delete_program(db, program_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Program not found")
    return None
