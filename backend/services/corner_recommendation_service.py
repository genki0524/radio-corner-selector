"""
コーナー推薦サービス
ベクトル検索とLLM推論を組み合わせた推薦機能
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from cruds.corner_repository_impl import CornerRepositoryImpl
from services.langchain_service import get_embedding_service, get_llm_service
from domain.services.corner_recommendation_service import CornerRecommendationService


class CornerRecommendationApplicationService:
    """コーナー推薦アプリケーションサービス"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = CornerRepositoryImpl(db)
        self.embedding_service = get_embedding_service()
        self.llm_service = get_llm_service()
        self.domain_service = CornerRecommendationService()
    
    def recommend_corners_for_memo(
        self,
        memo_content: str,
        user_id: int,
        top_k: int = 10,
        use_llm: bool = True,
        final_results: int = 3
    ) -> Dict:
        """
        メモ内容から最適なコーナーを推薦
        
        Args:
            memo_content: メモの内容
            user_id: ユーザーID
            top_k: ベクトル検索で取得する候補数
            use_llm: LLM推論を使用するか
            final_results: 最終的に返却する推薦数
            
        Returns:
            推薦結果（recommendations, metadata）
        """
        # 1. メモ内容を埋め込みベクトルに変換
        query_vector = self.embedding_service.embed_text(memo_content)
        
        # 2. ベクトル類似度検索で候補を取得
        vector_results = self.repository.find_by_vector_similarity(
            query_vector=query_vector,
            user_id=user_id,
            limit=top_k
        )
        
        if not vector_results:
            return {
                "recommendations": [],
                "metadata": {
                    "memo_content": memo_content,
                    "method": "vector_search",
                    "candidates_found": 0
                }
            }
        
        # 3. LLM推論を使用する場合
        if use_llm:
            # LLMで各候補を評価
            llm_result = self.llm_service.recommend_corner(
                memo_content=memo_content,
                candidate_corners=vector_results,
                max_candidates=min(top_k, 5)  # LLMには最大5件
            )
            
            # ベクトル検索結果とLLM評価を統合
            # LLMの推薦結果を反映
            for result in vector_results:
                if result["id"] == llm_result.get("corner_id"):
                    result["llm_score"] = llm_result.get("score", 0.5)
                    result["reasoning"] = llm_result.get("reasoning", "")
                else:
                    result["llm_score"] = 0.3  # その他の候補はデフォルトスコア
                
                # 統合スコアを計算
                result["score"] = self.domain_service.combine_scores(
                    similarity=result["similarity"],
                    llm_score=result["llm_score"]
                )
                result["confidence"] = self.domain_service.evaluate_recommendation_quality(
                    result["score"]
                )
            
            method = "vector_search_with_llm"
        else:
            # ベクトル検索のみの場合
            for result in vector_results:
                result["score"] = result["similarity"]
                result["confidence"] = self.domain_service.evaluate_recommendation_quality(
                    result["score"]
                )
            method = "vector_search_only"
        
        # 4. スコアでランキング
        ranked_results = self.domain_service.rank_recommendations(
            vector_results,
            max_results=final_results
        )
        
        # 5. 結果を整形
        return {
            "recommendations": ranked_results,
            "metadata": {
                "memo_content": memo_content,
                "method": method,
                "candidates_found": len(vector_results),
                "top_results": len(ranked_results)
            }
        }
    
    def recommend_single_best_corner(
        self,
        memo_content: str,
        user_id: int
    ) -> Optional[Dict]:
        """
        メモ内容から最も適したコーナーを1つ推薦
        
        Args:
            memo_content: メモの内容
            user_id: ユーザーID
            
        Returns:
            最適なコーナー情報
        """
        result = self.recommend_corners_for_memo(
            memo_content=memo_content,
            user_id=user_id,
            top_k=5,
            use_llm=True,
            final_results=1
        )
        
        recommendations = result.get("recommendations", [])
        return recommendations[0] if recommendations else None
    
    def batch_recommend_for_memos(
        self,
        memos: List[Dict],
        user_id: int
    ) -> List[Dict]:
        """
        複数メモに対して一括推薦
        
        Args:
            memos: メモのリスト [{"id": 1, "content": "..."}]
            user_id: ユーザーID
            
        Returns:
            各メモの推薦結果
        """
        results = []
        
        for memo in memos:
            recommendation = self.recommend_single_best_corner(
                memo_content=memo["content"],
                user_id=user_id
            )
            
            results.append({
                "memo_id": memo["id"],
                "memo_content": memo["content"],
                "recommendation": recommendation
            })
        
        return results
    
    def update_corner_embedding(self, corner_id: int) -> bool:
        """
        コーナーの埋め込みベクトルを更新
        
        Args:
            corner_id: コーナーID
            
        Returns:
            更新成功可否
        """
        # コーナーを取得
        from models import Corner
        corner = self.db.query(Corner).filter(Corner.id == corner_id).first()
        
        if not corner:
            return False
        
        # description_for_llmから埋め込みを生成
        embedding = self.embedding_service.embed_text(corner.description_for_llm)
        
        # 埋め込みを更新
        corner.embedded_description = embedding
        self.db.commit()
        
        return True
    
    def bulk_update_embeddings(self, user_id: Optional[int] = None) -> Dict:
        """
        全コーナーまたは特定ユーザーのコーナーの埋め込みを一括更新
        
        Args:
            user_id: ユーザーID（指定しない場合は全コーナー）
            
        Returns:
            更新結果の統計情報
        """
        from models import Corner, Program
        
        # クエリを構築
        query = self.db.query(Corner)
        if user_id:
            query = query.join(Program).filter(Program.user_id == user_id)
        
        corners = query.all()
        
        updated_count = 0
        failed_count = 0
        
        for corner in corners:
            try:
                # 埋め込みを生成
                embedding = self.embedding_service.embed_text(corner.description_for_llm)
                corner.embedded_description = embedding
                updated_count += 1
            except Exception as e:
                print(f"Failed to update corner {corner.id}: {e}")
                failed_count += 1
        
        # 一括コミット
        self.db.commit()
        
        return {
            "total_corners": len(corners),
            "updated": updated_count,
            "failed": failed_count
        }


def get_recommendation_service(db: Session) -> CornerRecommendationApplicationService:
    """推薦サービスのインスタンスを取得"""
    return CornerRecommendationApplicationService(db)
