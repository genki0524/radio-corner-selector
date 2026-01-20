"""
リポジトリインターフェース: コーナー
データアクセスの抽象化
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from domain.entities.corner_entity import CornerEntity


class CornerRepositoryInterface(ABC):
    """コーナーリポジトリのインターフェース"""
    
    @abstractmethod
    def find_by_id(self, corner_id: int) -> Optional[CornerEntity]:
        """IDでコーナーを取得"""
        pass
    
    @abstractmethod
    def find_by_program_id(self, program_id: int) -> List[CornerEntity]:
        """番組IDでコーナー一覧を取得"""
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[CornerEntity]:
        """ユーザーIDで全コーナーを取得"""
        pass
    
    @abstractmethod
    def save(self, corner: CornerEntity) -> CornerEntity:
        """コーナーを保存"""
        pass
    
    @abstractmethod
    def delete(self, corner_id: int) -> bool:
        """コーナーを削除"""
        pass
    
    @abstractmethod
    def find_by_vector_similarity(
        self,
        query_vector: List[float],
        user_id: int,
        limit: int = 10
    ) -> List[Dict]:
        """
        ベクトル類似度検索
        
        Args:
            query_vector: 検索クエリベクトル
            user_id: ユーザーID（検索範囲を限定）
            limit: 返却する最大件数
            
        Returns:
            類似度順のコーナーリスト（similarity含む）
        """
        pass
