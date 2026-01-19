"""
リポジトリインターフェース: メモ
データアクセスの抽象化
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.memo_entity import MemoEntity


class MemoRepositoryInterface(ABC):
    """メモリポジトリのインターフェース"""
    
    @abstractmethod
    def find_by_id(self, memo_id: int) -> Optional[MemoEntity]:
        """IDでメモを取得"""
        pass
    
    @abstractmethod
    def find_by_user_id(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[MemoEntity]:
        """ユーザーIDでメモ一覧を取得"""
        pass
    
    @abstractmethod
    def save(self, memo: MemoEntity) -> MemoEntity:
        """メモを保存"""
        pass
    
    @abstractmethod
    def delete(self, memo_id: int) -> bool:
        """メモを削除"""
        pass
