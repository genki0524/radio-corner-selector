"""
メール管理API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import MailCreate, MailUpdate, MailResponse, MailStatsResponse
from services import mail_service

router = APIRouter(prefix="/mails", tags=["mails"])


@router.get("", response_model=List[MailResponse])
def get_mails(
    user_id: int,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """メール一覧を取得"""
    return mail_service.get_mails(db, user_id, status_filter, skip, limit)


@router.get("/stats", response_model=MailStatsResponse)
def get_mail_stats(user_id: int, db: Session = Depends(get_db)):
    """メール統計を取得"""
    stats = mail_service.get_mail_stats(db, user_id)
    return MailStatsResponse(**stats)


@router.get("/{mail_id}", response_model=MailResponse)
def get_mail(mail_id: int, db: Session = Depends(get_db)):
    """メールを取得"""
    mail = mail_service.get_mail(db, mail_id)
    if not mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
    return mail


@router.post("", response_model=MailResponse, status_code=status.HTTP_201_CREATED)
def create_mail(mail: MailCreate, db: Session = Depends(get_db)):
    """メールを作成"""
    return mail_service.create_mail(db, mail)


@router.put("/{mail_id}", response_model=MailResponse)
def update_mail(mail_id: int, mail: MailUpdate, db: Session = Depends(get_db)):
    """メールを更新"""
    db_mail = mail_service.update_mail(db, mail_id, mail)
    if not db_mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
    return db_mail


@router.delete("/{mail_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mail(mail_id: int, db: Session = Depends(get_db)):
    """メールを削除"""
    if not mail_service.delete_mail(db, mail_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
    return None
