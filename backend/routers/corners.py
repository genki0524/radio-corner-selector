"""
コーナー管理API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import CornerCreate, CornerUpdate, CornerResponse
from services import corner_service

router = APIRouter(prefix="/corners", tags=["corners"])


@router.get("", response_model=List[CornerResponse])
def get_corners(program_id: int, db: Session = Depends(get_db)):
    """コーナー一覧を取得"""
    return corner_service.get_corners(db, program_id)


@router.get("/{corner_id}", response_model=CornerResponse)
def get_corner(corner_id: int, db: Session = Depends(get_db)):
    """コーナーを取得"""
    corner = corner_service.get_corner(db, corner_id)
    if not corner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Corner not found")
    return corner


@router.post("", response_model=CornerResponse, status_code=status.HTTP_201_CREATED)
def create_corner(corner: CornerCreate, db: Session = Depends(get_db)):
    """コーナーを作成"""
    return corner_service.create_corner(db, corner)


@router.put("/{corner_id}", response_model=CornerResponse)
def update_corner(corner_id: int, corner: CornerUpdate, db: Session = Depends(get_db)):
    """コーナーを更新"""
    db_corner = corner_service.update_corner(db, corner_id, corner)
    if not db_corner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Corner not found")
    return db_corner


@router.delete("/{corner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_corner(corner_id: int, db: Session = Depends(get_db)):
    """コーナーを削除"""
    if not corner_service.delete_corner(db, corner_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Corner not found")
    return None
