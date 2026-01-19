"""
リポジトリインターフェース: 番組
データアクセスの抽象化
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.program_entity import ProgramEntity


class ProgramRepositoryInterface(ABC):
    """番組リポジトリのインターフェース"""
    
    @abstractmethod
    def find_by_id(self, program_id: int) -> Optional[ProgramEntity]:
        """IDで番組を取得"""
        pass
    
    @abstractmethod
    def find_by_user_id(
        self,
        user_id: int,
        personality_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[ProgramEntity]:
        """ユーザーIDで番組一覧を取得"""
        pass
    
    @abstractmethod
    def save(self, program: ProgramEntity) -> ProgramEntity:
        """番組を保存"""
        pass
    
    @abstractmethod
    def delete(self, program_id: int) -> bool:
        """番組を削除"""
        pass
