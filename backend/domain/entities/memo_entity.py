"""
ドメインエンティティ: メモ
"""
from datetime import datetime
from typing import Optional


class MemoEntity:
    """メモのドメインエンティティ"""
    
    def __init__(
        self,
        id: int,
        user_id: int,
        content: str,
        created_at: datetime
    ):
        self._id = id
        self._user_id = user_id
        self._content = content
        self._created_at = created_at
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def user_id(self) -> int:
        return self._user_id
    
    @property
    def content(self) -> str:
        return self._content
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    def update_content(self, new_content: str) -> None:
        """メモ内容を更新"""
        if not new_content or not new_content.strip():
            raise ValueError("Memo content cannot be empty")
        self._content = new_content
    
    def is_empty(self) -> bool:
        """メモが空かどうか判定"""
        return not self._content or not self._content.strip()
    
    def get_word_count(self) -> int:
        """文字数を取得"""
        return len(self._content)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, MemoEntity):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
