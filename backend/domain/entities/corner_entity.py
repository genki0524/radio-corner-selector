"""
ドメインエンティティ: コーナー
"""
from typing import Optional


class CornerEntity:
    """コーナーのドメインエンティティ"""
    
    def __init__(
        self,
        id: int,
        program_id: int,
        title: str,
        description_for_llm: str
    ):
        self._id = id
        self._program_id = program_id
        self._title = title
        self._description_for_llm = description_for_llm
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def program_id(self) -> int:
        return self._program_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description_for_llm(self) -> str:
        return self._description_for_llm
    
    def update_info(
        self,
        title: Optional[str] = None,
        description_for_llm: Optional[str] = None
    ) -> None:
        """コーナー情報を更新"""
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            self._title = title
        
        if description_for_llm is not None:
            if not description_for_llm.strip():
                raise ValueError("Description for LLM cannot be empty")
            self._description_for_llm = description_for_llm
    
    def has_sufficient_description(self, min_length: int = 10) -> bool:
        """LLM用説明が十分かどうか判定"""
        return len(self._description_for_llm.strip()) >= min_length
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CornerEntity):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
