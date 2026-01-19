"""
ドメインサービス: コーナー推奨
LLM解析結果の評価とランキング
"""
from typing import List, Dict
from domain.value_objects.recommendation_score import RecommendationScore


class CornerRecommendationService:
    """コーナー推奨に関するドメインサービス"""
    
    @staticmethod
    def rank_recommendations(
        recommendations: List[Dict],
        max_results: int = 3
    ) -> List[Dict]:
        """
        推奨結果をランキング
        
        Args:
            recommendations: 推奨結果のリスト
            max_results: 返却する最大件数
        
        Returns:
            スコア順にソートされた推奨結果
        """
        # スコアでソート（降順）
        sorted_recs = sorted(
            recommendations,
            key=lambda r: r.get("score", 0.0),
            reverse=True
        )
        
        return sorted_recs[:max_results]
    
    @staticmethod
    def filter_by_confidence(
        recommendations: List[Dict],
        min_score: float = 0.3
    ) -> List[Dict]:
        """
        信頼度でフィルタリング
        
        Args:
            recommendations: 推奨結果のリスト
            min_score: 最小スコア閾値
        
        Returns:
            閾値以上のスコアを持つ推奨結果
        """
        return [
            rec for rec in recommendations
            if rec.get("score", 0.0) >= min_score
        ]
    
    @staticmethod
    def evaluate_recommendation_quality(score_value: float) -> str:
        """
        推奨品質を評価
        
        Args:
            score_value: スコア値
        
        Returns:
            評価ラベル（高/中/低）
        """
        score = RecommendationScore(score_value)
        
        if score.is_high_confidence(0.8):
            return "高信頼度"
        elif score.is_low_confidence(0.3):
            return "低信頼度"
        else:
            return "中信頼度"
    
    @staticmethod
    def should_show_warning(score_value: float) -> bool:
        """
        警告を表示すべきか判定
        
        Args:
            score_value: スコア値
        
        Returns:
            警告表示が必要かどうか
        """
        score = RecommendationScore(score_value)
        return score.is_low_confidence(0.5)
