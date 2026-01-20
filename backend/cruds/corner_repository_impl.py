"""
コーナーリポジトリ実装
Repository Interfaceの具体的な実装
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text

from models import Corner, Program
from domain.repositories.corner_repository import CornerRepositoryInterface
from domain.entities.corner_entity import CornerEntity


class CornerRepositoryImpl(CornerRepositoryInterface):
    """コーナーリポジトリの実装クラス"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def find_by_id(self, corner_id: int) -> Optional[CornerEntity]:
        """IDでコーナーを取得"""
        db_corner = self._db.query(Corner).filter(Corner.id == corner_id).first()
        if not db_corner:
            return None
        return self._to_entity(db_corner)
    
    def find_by_program_id(self, program_id: int) -> List[CornerEntity]:
        """番組IDでコーナー一覧を取得"""
        db_corners = (
            self._db.query(Corner)
            .filter(Corner.program_id == program_id)
            .all()
        )
        return [self._to_entity(corner) for corner in db_corners]
    
    def find_by_user_id(self, user_id: int) -> List[CornerEntity]:
        """ユーザーIDで全コーナーを取得"""
        db_corners = (
            self._db.query(Corner)
            .join(Program, Corner.program_id == Program.id)
            .filter(Program.user_id == user_id)
            .all()
        )
        return [self._to_entity(corner) for corner in db_corners]
    
    def save(self, corner: CornerEntity) -> CornerEntity:
        """コーナーを保存（新規作成または更新）"""
        db_corner = self._db.query(Corner).filter(Corner.id == corner.id).first()
        
        if db_corner:
            # 更新
            db_corner.title = corner.title
            db_corner.description_for_llm = corner.description_for_llm
        else:
            # 新規作成
            db_corner = Corner(
                id=corner.id,
                program_id=corner.program_id,
                title=corner.title,
                description_for_llm=corner.description_for_llm
            )
            self._db.add(db_corner)
        
        self._db.commit()
        self._db.refresh(db_corner)
        return self._to_entity(db_corner)
    
    def delete(self, corner_id: int) -> bool:
        """コーナーを削除"""
        db_corner = self._db.query(Corner).filter(Corner.id == corner_id).first()
        if not db_corner:
            return False
        
        self._db.delete(db_corner)
        self._db.commit()
        return True
    
    def create_from_dict(self, corner_data: dict) -> Corner:
        """辞書からコーナーを作成（後方互換性のため）"""
        db_corner = Corner(**corner_data)
        self._db.add(db_corner)
        self._db.commit()
        self._db.refresh(db_corner)
        return db_corner
    
    def update_from_dict(self, corner_id: int, corner_data: dict) -> Optional[Corner]:
        """辞書でコーナーを更新（後方互換性のため）"""
        db_corner = self._db.query(Corner).filter(Corner.id == corner_id).first()
        if not db_corner:
            return None
        
        for key, value in corner_data.items():
            setattr(db_corner, key, value)
        
        self._db.commit()
        self._db.refresh(db_corner)
        return db_corner
    
    def get_by_id(self, corner_id: int) -> Optional[Corner]:
        """IDでコーナーを取得（後方互換性のため）"""
        return self._db.query(Corner).filter(Corner.id == corner_id).first()
    
    def get_by_program_id(self, program_id: int) -> List[Corner]:
        """番組IDでコーナー一覧を取得（後方互換性のため）"""
        return self._db.query(Corner).filter(Corner.program_id == program_id).all()
    
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
        # pgvectorの<=>演算子を使用してコサイン距離を計算
        # コサイン距離 = 1 - コサイン類似度なので、類似度に変換
        query = text("""
            SELECT 
                c.id,
                c.title,
                c.description_for_llm,
                c.program_id,
                1 - (c.embedded_description <=> :query_vector) as similarity
            FROM corners c
            JOIN programs p ON c.program_id = p.id
            WHERE p.user_id = :user_id
            ORDER BY c.embedded_description <=> :query_vector
            LIMIT :limit
        """)
        
        result = self._db.execute(
            query,
            {
                "query_vector": query_vector,
                "user_id": user_id,
                "limit": limit
            }
        )
        
        corners = []
        for row in result:
            corners.append({
                "id": row.id,
                "title": row.title,
                "description_for_llm": row.description_for_llm,
                "program_id": row.program_id,
                "similarity": float(row.similarity)
            })
        
        return corners
    
    @staticmethod
    def _to_entity(db_corner: Corner) -> CornerEntity:
        """DBモデルをエンティティに変換"""
        return CornerEntity(
            id=db_corner.id,
            program_id=db_corner.program_id,
            title=db_corner.title,
            description_for_llm=db_corner.description_for_llm
        )
