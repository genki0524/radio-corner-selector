"""
メモリポジトリ実装
Repository Interfaceの具体的な実装
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Memo
from domain.repositories.memo_repository import MemoRepositoryInterface
from domain.entities.memo_entity import MemoEntity


class MemoRepositoryImpl(MemoRepositoryInterface):
    """メモリポジトリの実装クラス"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def find_by_id(self, memo_id: int) -> Optional[MemoEntity]:
        """IDでメモを取得"""
        db_memo = self._db.query(Memo).filter(Memo.id == memo_id).first()
        if not db_memo:
            return None
        return self._to_entity(db_memo)
    
    def find_by_user_id(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[MemoEntity]:
        """ユーザーIDでメモ一覧を取得"""
        db_memos = (
            self._db.query(Memo)
            .filter(Memo.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(memo) for memo in db_memos]
    
    def save(self, memo: MemoEntity) -> MemoEntity:
        """メモを保存（新規作成または更新）"""
        db_memo = self._db.query(Memo).filter(Memo.id == memo.id).first()
        
        if db_memo:
            # 更新
            db_memo.content = memo.content
        else:
            # 新規作成
            db_memo = Memo(
                id=memo.id,
                user_id=memo.user_id,
                content=memo.content,
                created_at=memo.created_at
            )
            self._db.add(db_memo)
        
        self._db.commit()
        self._db.refresh(db_memo)
        return self._to_entity(db_memo)
    
    def delete(self, memo_id: int) -> bool:
        """メモを削除"""
        db_memo = self._db.query(Memo).filter(Memo.id == memo_id).first()
        if not db_memo:
            return False
        
        self._db.delete(db_memo)
        self._db.commit()
        return True
    
    def create_from_dict(self, memo_data: dict) -> Memo:
        """辞書からメモを作成（後方互換性のため）"""
        db_memo = Memo(**memo_data)
        self._db.add(db_memo)
        self._db.commit()
        self._db.refresh(db_memo)
        return db_memo
    
    def update_from_dict(self, memo_id: int, memo_data: dict) -> Optional[Memo]:
        """辞書でメモを更新（後方互換性のため）"""
        db_memo = self._db.query(Memo).filter(Memo.id == memo_id).first()
        if not db_memo:
            return None
        
        for key, value in memo_data.items():
            setattr(db_memo, key, value)
        
        self._db.commit()
        self._db.refresh(db_memo)
        return db_memo
    
    def get_by_id(self, memo_id: int) -> Optional[Memo]:
        """IDでメモを取得（後方互換性のため）"""
        return self._db.query(Memo).filter(Memo.id == memo_id).first()
    
    def get_by_user_id(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Memo]:
        """ユーザーIDでメモ一覧を取得（後方互換性のため）"""
        return (
            self._db.query(Memo)
            .filter(Memo.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def _to_entity(db_memo: Memo) -> MemoEntity:
        """DBモデルをエンティティに変換"""
        return MemoEntity(
            id=db_memo.id,
            user_id=db_memo.user_id,
            content=db_memo.content,
            created_at=db_memo.created_at
        )
