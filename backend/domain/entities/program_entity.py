"""
ドメインエンティティ: 番組
"""
from typing import List, Optional
from domain.value_objects.email_address import EmailAddress


class ProgramEntity:
    """番組のドメインエンティティ"""
    
    def __init__(
        self,
        id: int,
        user_id: int,
        title: str,
        email_address: Optional[EmailAddress] = None,
        broadcast_schedule: Optional[str] = None,
    ):
        self._id = id
        self._user_id = user_id
        self._title = title
        self._email_address = email_address
        self._broadcast_schedule = broadcast_schedule
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def user_id(self) -> int:
        return self._user_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def email_address(self) -> Optional[EmailAddress]:
        return self._email_address
    
    @property
    def broadcast_schedule(self) -> Optional[str]:
        return self._broadcast_schedule
    
    def update_info(
        self,
        title: Optional[str] = None,
        email_address: Optional[EmailAddress] = None,
        broadcast_schedule: Optional[str] = None
    ) -> None:
        """番組情報を更新"""
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            self._title = title
        
        if email_address is not None:
            self._email_address = email_address
        
        if broadcast_schedule is not None:
            self._broadcast_schedule = broadcast_schedule
    
    def has_email_address(self) -> bool:
        """投稿先メールアドレスが設定されているか"""
        return self._email_address is not None and self._email_address.value is not None
    
    def can_submit_mail(self) -> bool:
        """メール投稿が可能か"""
        return self.has_email_address()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ProgramEntity):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
