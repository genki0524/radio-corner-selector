"""
メモ管理API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import MemoCreate, MemoUpdate, MemoResponse
from services import memo_service

router = APIRouter(prefix="/memos", tags=["memos"])


@router.get("", response_model=List[MemoResponse])
def get_memos(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """メモ一覧を取得"""
    return memo_service.get_memos(db, user_id, skip, limit)


@router.get("/{memo_id}", response_model=MemoResponse)
def get_memo(memo_id: int, db: Session = Depends(get_db)):
    """メモを取得"""
    memo = memo_service.get_memo(db, memo_id)
    if not memo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")
    return memo


@router.post("", response_model=MemoResponse, status_code=status.HTTP_201_CREATED)
def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    """メモを作成"""
    return memo_service.create_memo(db, memo)


@router.put("/{memo_id}", response_model=MemoResponse)
def update_memo(memo_id: int, memo: MemoUpdate, db: Session = Depends(get_db)):
    """メモを更新"""
    db_memo = memo_service.update_memo(db, memo_id, memo)
    if not db_memo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")
    return db_memo


@router.delete("/{memo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    """メモを削除"""
    if not memo_service.delete_memo(db, memo_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")
    return None
