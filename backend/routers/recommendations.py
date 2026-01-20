"""
コーナー推薦APIルーター
ベクトル検索とLLM推論を使用した推薦エンドポイント
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    CornerRecommendationRequest,
    CornerRecommendationResult,
    UpdateEmbeddingRequest,
    UpdateEmbeddingResponse
)
from services.corner_recommendation_service import get_recommendation_service


router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.post("/corners", response_model=CornerRecommendationResult)
def recommend_corners(
    request: CornerRecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    メモ内容から最適なコーナーを推薦
    
    ベクトル検索とLLM推論を組み合わせて、メモ内容に最も適したコーナーを推薦します。
    
    - **memo_content**: メモの内容
    - **user_id**: ユーザーID
    - **top_k**: ベクトル検索で取得する候補数（1-50、デフォルト10）
    - **use_llm**: LLM推論を使用するか（デフォルトTrue）
    - **final_results**: 最終的に返却する推薦数（1-10、デフォルト3）
    """
    try:
        service = get_recommendation_service(db)
        result = service.recommend_corners_for_memo(
            memo_content=request.memo_content,
            user_id=request.user_id,
            top_k=request.top_k,
            use_llm=request.use_llm,
            final_results=request.final_results
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推薦処理でエラーが発生しました: {str(e)}")


@router.post("/corners/single")
def recommend_single_corner(
    memo_content: str,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    メモ内容から最も適したコーナーを1つ推薦
    
    - **memo_content**: メモの内容
    - **user_id**: ユーザーID
    """
    try:
        service = get_recommendation_service(db)
        result = service.recommend_single_best_corner(
            memo_content=memo_content,
            user_id=user_id
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="適切なコーナーが見つかりませんでした")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推薦処理でエラーが発生しました: {str(e)}")


@router.post("/embeddings/update", response_model=UpdateEmbeddingResponse)
def update_embeddings(
    request: UpdateEmbeddingRequest,
    db: Session = Depends(get_db)
):
    """
    コーナーの埋め込みベクトルを更新
    
    - **corner_id**: 特定のコーナーIDを指定（オプション）
    - **user_id**: ユーザーIDを指定して、そのユーザーのコーナーのみ更新（オプション）
    - 両方未指定の場合、全コーナーを更新
    """
    try:
        service = get_recommendation_service(db)
        
        if request.corner_id:
            # 特定のコーナーのみ更新
            success = service.update_corner_embedding(request.corner_id)
            if success:
                return UpdateEmbeddingResponse(
                    success=True,
                    message=f"コーナーID {request.corner_id} の埋め込みを更新しました"
                )
            else:
                return UpdateEmbeddingResponse(
                    success=False,
                    message=f"コーナーID {request.corner_id} が見つかりませんでした"
                )
        else:
            # 一括更新
            stats = service.bulk_update_embeddings(user_id=request.user_id)
            return UpdateEmbeddingResponse(
                success=True,
                message=f"{stats['updated']}件のコーナーの埋め込みを更新しました",
                details=stats
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"埋め込み更新でエラーが発生しました: {str(e)}")


@router.get("/health")
def health_check():
    """
    推薦システムのヘルスチェック
    
    LangChainサービスが正常に動作しているか確認します。
    """
    try:
        from services.langchain_service import get_embedding_service, get_llm_service
        
        # 埋め込みサービスのテスト
        embedding_service = get_embedding_service()
        test_embedding = embedding_service.embed_text("テスト")
        
        # LLMサービスの初期化確認
        llm_service = get_llm_service()
        
        return {
            "status": "healthy",
            "embedding_service": "ok",
            "embedding_dimension": len(test_embedding),
            "llm_service": "ok"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
