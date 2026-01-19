"""
メールサービス
ビジネスロジックを集約
Repository Interfaceを使用
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from cruds.mail_repository_impl import MailRepositoryImpl
from domain.repositories.mail_repository import MailRepositoryInterface
from schemas import MailCreate, MailUpdate, MailResponse


def _get_repository(db: Session) -> MailRepositoryInterface:
    """Repositoryインスタンスを取得（DI用）"""
    return MailRepositoryImpl(db)


def get_mails(
    db: Session,
    user_id: int,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[MailResponse]:
    """メール一覧を取得"""
    repo = _get_repository(db)
    return repo.get_by_user_id(user_id, status_filter, skip, limit)


def get_mail_stats(db: Session, user_id: int) -> dict:
    """メール統計を取得"""
    repo = _get_repository(db)
    return repo.get_statistics(user_id)


def get_mail(db: Session, mail_id: int) -> Optional[MailResponse]:
    """メールを取得"""
    repo = _get_repository(db)
    return repo.get_by_id(mail_id)


def create_mail(db: Session, mail: MailCreate) -> MailResponse:
    """メールを作成"""
    repo = _get_repository(db)
    return repo.create_from_dict(mail.model_dump())


def update_mail(
    db: Session,
    mail_id: int,
    mail: MailUpdate
) -> Optional[MailResponse]:
    """メールを更新"""
    repo = _get_repository(db)
    return repo.update_from_dict(mail_id, mail.model_dump(exclude_unset=True))


def delete_mail(db: Session, mail_id: int) -> bool:
    """メールを削除"""
    repo = _get_repository(db)
    return repo.delete(mail_id)
