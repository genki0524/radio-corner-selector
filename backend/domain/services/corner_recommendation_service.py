"""
ドメインサービス: コーナー推奨
LLM解析結果の評価とランキング
ベクトル検索とLLM推論を組み合わせた推薦
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
    def combine_scores(
        similarity: float,
        llm_score: float,
        similarity_weight: float = 0.4,
        llm_weight: float = 0.6
    ) -> float:
        """
        ベクトル類似度とLLMスコアを組み合わせる
        
        Args:
            similarity: ベクトル類似度スコア (0.0-1.0)
            llm_score: LLMによる評価スコア (0.0-1.0)
            similarity_weight: 類似度の重み
            llm_weight: LLMスコアの重み
            
        Returns:
            統合スコア (0.0-1.0)
        """
        # 重みを正規化
        total_weight = similarity_weight + llm_weight
        norm_sim_weight = similarity_weight / total_weight
        norm_llm_weight = llm_weight / total_weight
        
        # 加重平均
        combined = (similarity * norm_sim_weight) + (llm_score * norm_llm_weight)
        
        return max(0.0, min(1.0, combined))
    
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
    
    @staticmethod
    def enrich_recommendations_with_combined_scores(
        vector_results: List[Dict],
        llm_evaluations: List[Dict]
    ) -> List[Dict]:
        """
        ベクトル検索結果とLLM評価を統合
        
        Args:
            vector_results: ベクトル検索結果（similarity含む）
            llm_evaluations: LLM評価結果（llm_score含む）
            
        Returns:
            統合スコア付きの推薦結果
        """
        # LLMスコアをIDでマッピング
        llm_scores_map = {
            item["id"]: item.get("llm_score", 0.5)
            for item in llm_evaluations
        }
        
        enriched = []
        for result in vector_results:
            corner_id = result["id"]
            similarity = result.get("similarity", 0.0)
            llm_score = llm_scores_map.get(corner_id, 0.5)
            
            # 統合スコアを計算
            combined_score = CornerRecommendationService.combine_scores(
                similarity, llm_score
            )
            
            enriched.append({
                **result,
                "llm_score": llm_score,
                "similarity_score": similarity,
                "score": combined_score,
                "confidence": CornerRecommendationService.evaluate_recommendation_quality(combined_score)
            })
        
        return enriched
