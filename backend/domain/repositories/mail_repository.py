"""
リポジトリインターフェース: メール
データアクセスの抽象化
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.mail_entity import MailEntity


class MailRepositoryInterface(ABC):
    """メールリポジトリのインターフェース"""
    
    @abstractmethod
    def find_by_id(self, mail_id: int) -> Optional[MailEntity]:
        """IDでメールを取得"""
        pass
    
    @abstractmethod
    def find_by_user_id(
        self,
        user_id: int,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[MailEntity]:
        """ユーザーIDでメール一覧を取得"""
        pass
    
    @abstractmethod
    def save(self, mail: MailEntity) -> MailEntity:
        """メールを保存"""
        pass
    
    @abstractmethod
    def delete(self, mail_id: int) -> bool:
        """メールを削除"""
        pass
