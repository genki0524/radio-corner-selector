"""
バリューオブジェクト: コーナー推奨スコア
"""
from typing import Union


class RecommendationScore:
    """コーナー推奨スコアのバリューオブジェクト"""
    
    def __init__(self, score: Union[float, int]):
        if not 0.0 <= score <= 1.0:
            raise ValueError(f"Score must be between 0.0 and 1.0, got {score}")
        self._score = float(score)
    
    @property
    def value(self) -> float:
        """スコア値を取得"""
        return self._score
    
    def is_high_confidence(self, threshold: float = 0.8) -> bool:
        """高信頼度かどうか判定"""
        return self._score >= threshold
    
    def is_low_confidence(self, threshold: float = 0.3) -> bool:
        """低信頼度かどうか判定"""
        return self._score <= threshold
    
    def __str__(self) -> str:
        return f"{self._score:.2f}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, RecommendationScore):
            return False
        return abs(self._score - other._score) < 0.001
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, RecommendationScore):
            raise TypeError("Cannot compare RecommendationScore with non-RecommendationScore")
        return self._score < other._score
    
    def __hash__(self) -> int:
        return hash(self._score)
