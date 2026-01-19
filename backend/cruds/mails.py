"""
メールのCRUD操作
Repository実装の後方互換ラッパー
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Mail
from cruds.mail_repository_impl import MailRepositoryImpl


def get_mails(
    db: Session,
    user_id: int,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Mail]:
    """メール一覧を取得"""
    repo = MailRepositoryImpl(db)
    return repo.get_by_user_id(user_id, status_filter, skip, limit)


def get_mail_stats(db: Session, user_id: int) -> dict:
    """メール統計を取得"""
    repo = MailRepositoryImpl(db)
    return repo.get_statistics(user_id)


def get_mail(db: Session, mail_id: int) -> Optional[Mail]:
    """メールを取得"""
    repo = MailRepositoryImpl(db)
    return repo.get_by_id(mail_id)


def create_mail(db: Session, mail_data: dict) -> Mail:
    """メールを作成"""
    repo = MailRepositoryImpl(db)
    return repo.create_from_dict(mail_data)


def update_mail(db: Session, mail_id: int, mail_data: dict) -> Optional[Mail]:
    """メールを更新"""
    repo = MailRepositoryImpl(db)
    return repo.update_from_dict(mail_id, mail_data)


def delete_mail(db: Session, mail_id: int) -> bool:
    """メールを削除"""
    repo = MailRepositoryImpl(db)
    return repo.delete(mail_id)