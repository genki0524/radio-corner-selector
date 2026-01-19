"""
LLM解析API
Google Gemini APIを使用してメモの内容を解析し、最適なコーナーを推奨
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import AnalyzeRequest, AnalyzeResponse, CornerRecommendation
from services import analyze_service

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.post("", response_model=AnalyzeResponse)
def analyze_memo(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    メモを解析して最適なコーナーを推奨
    """
    # サービス層で解析処理を実行
    result = analyze_service.analyze_memo_for_corners(db, request.memo_id, request.user_id)
    
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["error"]
        )
    
    # レスポンス形式に変換
    recommendations = [
        CornerRecommendation(**rec)
        for rec in result["recommendations"]
    ]
    
    return AnalyzeResponse(
        memo_id=result["memo_id"],
        recommendations=recommendations,
    )
