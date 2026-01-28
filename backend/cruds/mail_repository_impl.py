"""
メールリポジトリ実装
Repository Interfaceの具体的な実装
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Mail
from models import Corner, Program
from domain.repositories.mail_repository import MailRepositoryInterface
from domain.entities.mail_entity import MailEntity
from domain.value_objects.mail_status import MailStatus


class MailRepositoryImpl(MailRepositoryInterface):
    """メールリポジトリの実装クラス"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def find_by_id(self, mail_id: int) -> Optional[MailEntity]:
        """IDでメールを取得"""
        db_mail = self._db.query(Mail).filter(Mail.id == mail_id).first()
        if not db_mail:
            return None
        return self._to_entity(db_mail)
    
    def find_by_user_id(
        self,
        user_id: int,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[MailEntity]:
        """ユーザーIDでメール一覧を取得"""
        
        query = (
            self._db.query(Mail)
            .join(Corner, Mail.corner_id == Corner.id)
            .join(Program, Corner.program_id == Program.id)
            .filter(Program.user_id == user_id)
        )
        
        if status_filter:
            query = query.filter(Mail.status == status_filter)
        
        db_mails = query.offset(skip).limit(limit).all()
        return [self._to_entity(mail) for mail in db_mails]
    
    def save(self, mail: MailEntity) -> MailEntity:
        """メールを保存（新規作成または更新）"""
        db_mail = self._db.query(Mail).filter(Mail.id == mail.id).first()
        
        if db_mail:
            # 更新
            db_mail.subject = mail.subject
            db_mail.body = mail.body
            db_mail.status = mail.status.value
            db_mail.sent_at = mail.sent_at
            db_mail.updated_at = mail.updated_at
        else:
            # 新規作成
            db_mail = Mail(
                id=mail.id,
                corner_id=mail.corner_id,
                memo_id=mail.memo_id,
                subject=mail.subject,
                body=mail.body,
                status=mail.status.value,
                sent_at=mail.sent_at,
                created_at=mail.created_at,
                updated_at=mail.updated_at
            )
            self._db.add(db_mail)
        
        self._db.commit()
        self._db.refresh(db_mail)
        return self._to_entity(db_mail)
    
    def delete(self, mail_id: int) -> bool:
        """メールを削除"""
        db_mail = self._db.query(Mail).filter(Mail.id == mail_id).first()
        if not db_mail:
            return False
        
        self._db.delete(db_mail)
        self._db.commit()
        return True
    
    def create_from_dict(self, mail_data: dict) -> Mail:
        """辞書からメールを作成（後方互換性のため）"""
        db_mail = Mail(**mail_data)
        self._db.add(db_mail)
        self._db.commit()
        self._db.refresh(db_mail)
        return db_mail
    
    def update_from_dict(self, mail_id: int, mail_data: dict) -> Optional[Mail]:
        """辞書でメールを更新（後方互換性のため）"""
        db_mail = self._db.query(Mail).filter(Mail.id == mail_id).first()
        if not db_mail:
            return None
        
        for key, value in mail_data.items():
            setattr(db_mail, key, value)
        
        self._db.commit()
        self._db.refresh(db_mail)
        return db_mail
    
    def get_by_id(self, mail_id: int) -> Optional[Mail]:
        """IDでメールを取得（後方互換性のため）"""
        return self._db.query(Mail).filter(Mail.id == mail_id).first()
    
    def get_by_user_id(
        self,
        user_id: int,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Mail]:
        """ユーザーIDでメール一覧を取得（後方互換性のため）"""
        from models import Corner, Program
        
        query = (
            self._db.query(Mail)
            .join(Corner, Mail.corner_id == Corner.id)
            .join(Program, Corner.program_id == Program.id)
            .filter(Program.user_id == user_id)
        )
        
        if status_filter:
            query = query.filter(Mail.status == status_filter)
        
        return query.offset(skip).limit(limit).all()
    
    def get_statistics(self, user_id: int) -> dict:
        """メール統計を取得（後方互換性のため）"""
        from models import Corner, Program
        from sqlalchemy import func
        
        mails = (
            self._db.query(Mail)
            .join(Corner, Mail.corner_id == Corner.id)
            .join(Program, Corner.program_id == Program.id)
            .filter(Program.user_id == user_id)
            .all()
        )
        
        total = len(mails)
        draft = sum(1 for m in mails if m.status == "下書き")
        sent = sum(1 for m in mails if m.status == "送信済み")
        accepted = sum(1 for m in mails if m.status == "採用")
        rejected = sum(1 for m in mails if m.status == "不採用")
        
        return {
            "total": total,
            "draft": draft,
            "sent": sent,
            "accepted": accepted,
            "rejected": rejected
        }
    
    @staticmethod
    def _to_entity(db_mail: Mail) -> MailEntity:
        """DBモデルをエンティティに変換"""
        return MailEntity(
            id=db_mail.id,
            corner_id=db_mail.corner_id,
            memo_id=db_mail.memo_id,
            subject=db_mail.subject,
            body=db_mail.body,
            status=MailStatus.from_string(db_mail.status),
            sent_at=db_mail.sent_at,
            created_at=db_mail.created_at,
            updated_at=db_mail.updated_at
        )
