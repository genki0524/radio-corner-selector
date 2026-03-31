"""
メモ解析サービス
Google Gemini APIを使用してメモの内容を解析し、最適なコーナーを推奨
"""

import json
import logging
from typing import List

from google import genai
from google.genai import errors as genai_errors
from sqlalchemy.orm import Session

from config import settings
from cruds import analyze as analyze_crud
from services.langchain_service import get_embedding_service

logger = logging.getLogger(__name__)


def _fallback_recommendation(corners_info: List[dict], reason: str) -> List[dict]:
    """エラー時のフォールバック推薦（ベクトル検索の先頭候補を返す）"""
    if not corners_info:
        return []
    return [{"corner_id": corners_info[0]["id"], "score": 0.0, "reason": reason}]


def analyze_memo_with_gemini(memo_content: str, corners_info: List[dict]) -> List[dict]:
    """
    Gemini APIを使用してメモを解析

    Args:
        memo_content: メモの内容
        corners_info: コーナー情報のリスト

    Returns:
        推奨コーナーのリスト
    """
    if not settings.gemini_api_key:
        logger.warning("Gemini APIキーが設定されていません。フォールバックを返します。")
        return _fallback_recommendation(corners_info, "APIキーが未設定のため、ベクトル検索の結果を使用しています。")

    client = genai.Client()

    corners_text = "\n\n".join(
        [
            f"ID: {c['id']}\n番組: {c['program_title']}\nコーナー: {c['corner_title']}\n説明: {c['description']}"
            for c in corners_info
        ]
    )

    prompt = f"""
以下のメモ内容を分析し、最適な投稿先コーナーを推奨してください。

【メモ内容】
{memo_content}

【投稿可能なコーナー一覧】
{corners_text}

【出力形式】
以下のJSON形式で、適合度の高い順に最大3つのコーナーを推奨してください：
```json
[
  {{
    "corner_id": コーナーID（数値）,
    "score": 適合度スコア（0.0-1.0の小数）,
    "reason": "推奨理由（100文字以内の日本語）"
  }}
]
```

注意点：
- scoreは0.0から1.0の範囲で、小数点第2位まで
- reasonは具体的で簡潔に
- 適合度の高い順にソート
- JSONのみを返し、他のテキストは含めない
"""

    try:
        response = client.models.generate_content(
            model=settings.gemini_model, contents=prompt
        )
    except genai_errors.ClientError as e:
        logger.error("Gemini APIクライアントエラー (status=%s): %s", e.status_code, e)
        return _fallback_recommendation(corners_info, "APIエラーが発生しました。手動で選択してください。")
    except genai_errors.ServerError as e:
        logger.error("Gemini APIサーバーエラー (status=%s): %s", e.status_code, e)
        return _fallback_recommendation(corners_info, "APIサーバーエラーが発生しました。手動で選択してください。")

    if not response.text:
        logger.warning("Gemini APIのレスポンスが空です（安全フィルターによりブロックされた可能性があります）")
        return _fallback_recommendation(corners_info, "レスポンスが取得できませんでした。手動で選択してください。")

    # レスポンスをパース
    response_text = response.text.strip()
    # ```json ... ``` を削除
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]

    try:
        return json.loads(response_text.strip())
    except json.JSONDecodeError as e:
        logger.error("GeminiレスポンスのJSONパースに失敗しました: %s\nレスポンス: %s", e, response_text)
        return _fallback_recommendation(corners_info, "レスポンスの解析に失敗しました。手動で選択してください。")


def analyze_memo_with_vector_search(
    db: Session, user_id: int, memo_content: str, max_candidates: int = 10
) -> List[dict]:
    """
    ベクトル検索を使用してメモを解析

    Args:
        db: データベースセッション
        user_id: ユーザーID
        memo_content: メモの内容
        max_candidates: 最大候補数
    Returns:
        類似度の高いコーナーのリスト
    """
    embedding_service = get_embedding_service()
    embedded_memo = embedding_service.embed_text(memo_content)

    similarity_threshold = 0.08
    rows = analyze_crud.search_corners_by_embedding(
        db, user_id, embedded_memo, similarity_threshold, max_candidates
    )

    return [
        {
            "id": row.id,
            "program_id": row.program_id,
            "title": row.title,
            "description_for_llm": row.description_for_llm,
            "program_title": row.program_title,
            "similarity": row.similarity,
        }
        for row in rows
    ]


def analyze_memo_for_corners(db: Session, memo_id: int, user_id: int) -> dict:
    """
    メモを解析して最適なコーナーを推奨するビジネスロジック

    Args:
        db: データベースセッション
        memo_id: メモID
        user_id: ユーザーID

    Returns:
        解析結果の辞書
    """
    # メモを取得
    memo = analyze_crud.get_memo_by_id(db, memo_id)
    if not memo:
        return None

    # ベクトル検索で類似コーナーを取得
    vector_search_results = analyze_memo_with_vector_search(db, user_id, memo.content, 10)

    if not vector_search_results:
        return {"memo_id": memo_id, "recommendations": [], "error": "No matching corners found"}

    # Gemini用のコーナー情報を整形
    corners_info = [
        {
            "id": result["id"],
            "program_id": result["program_id"],
            "program_title": result["program_title"],
            "corner_title": result["title"],
            "description": result["description_for_llm"],
        }
        for result in vector_search_results
    ]

    # Gemini APIで解析
    llm_recommendations = analyze_memo_with_gemini(memo.content, corners_info)

    # レスポンス形式に変換
    recommendations = []
    for rec in llm_recommendations:
        corner_info = next(
            (c for c in corners_info if c["id"] == rec["corner_id"]), None
        )
        if corner_info:
            recommendations.append(
                {
                    "corner_id": rec["corner_id"],
                    "corner_title": corner_info["corner_title"],
                    "program_id": corner_info["program_id"],
                    "program_title": corner_info["program_title"],
                    "score": rec["score"],
                    "reason": rec["reason"],
                }
            )

    return {
        "memo_id": memo.id,
        "recommendations": recommendations,
    }
