"""
ドメインエンティティ: メール
"""
from datetime import datetime
from typing import Optional
from domain.value_objects.mail_status import MailStatus


class MailEntity:
    """メールのドメインエンティティ"""
    
    def __init__(
        self,
        id: int,
        user_id: int,
        subject: str,
        body: str,
        status: MailStatus,
        corner_id: Optional[int] = None,
        memo_id: Optional[int] = None,
        sent_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = id
        self._user_id = user_id
        self._corner_id = corner_id
        self._memo_id = memo_id
        self._subject = subject
        self._body = body
        self._status = status
        self._sent_at = sent_at
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def user_id(self) -> int:
        return self._user_id
    
    @property
    def corner_id(self) -> Optional[int]:
        return self._corner_id
    
    @property
    def memo_id(self) -> Optional[int]:
        return self._memo_id
    
    @property
    def subject(self) -> str:
        return self._subject
    
    @property
    def body(self) -> str:
        return self._body
    
    @property
    def status(self) -> MailStatus:
        return self._status
    
    @property
    def sent_at(self) -> Optional[datetime]:
        return self._sent_at
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def update_content(self, subject: Optional[str] = None, body: Optional[str] = None) -> None:
        """メール内容を更新"""
        if subject is not None:
            if not subject.strip():
                raise ValueError("Subject cannot be empty")
            self._subject = subject
        
        if body is not None:
            if not body.strip():
                raise ValueError("Body cannot be empty")
            self._body = body
        
        self._updated_at = datetime.now()
    
    def change_status(self, new_status: MailStatus) -> None:
        """ステータスを変更"""
        if not self._status.can_transition_to(new_status):
            raise ValueError(
                f"Cannot transition from {self._status.value} to {new_status.value}"
            )
        
        self._status = new_status
        self._updated_at = datetime.now()
        
        # 送信済みに変更した場合、送信日時を記録
        if new_status == MailStatus.SENT and not self._sent_at:
            self._sent_at = datetime.now()
    
    def mark_as_sent(self) -> None:
        """送信済みにマーク"""
        self.change_status(MailStatus.SENT)
    
    def mark_as_accepted(self) -> None:
        """採用にマーク"""
        self.change_status(MailStatus.ACCEPTED)
    
    def mark_as_rejected(self) -> None:
        """不採用にマーク"""
        self.change_status(MailStatus.REJECTED)
    
    def is_draft(self) -> bool:
        """下書きかどうか"""
        return self._status == MailStatus.DRAFT
    
    def is_sent(self) -> bool:
        """送信済みかどうか"""
        return self._status == MailStatus.SENT
    
    def can_edit(self) -> bool:
        """編集可能かどうか"""
        return self._status == MailStatus.DRAFT
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, MailEntity):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
