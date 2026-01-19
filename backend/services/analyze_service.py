"""
メモ解析サービス
Google Gemini APIを使用してメモの内容を解析し、最適なコーナーを推奨
"""
from typing import List
import json
import google.generativeai as genai
from sqlalchemy.orm import Session

from config import settings
from cruds import analyze as analyze_crud

# Gemini APIの設定
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)


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
        # APIキーが設定されていない場合はモックデータを返す
        return [
            {
                "corner_id": corners_info[0]["id"],
                "score": 0.85,
                "reason": "メモの内容がこのコーナーの趣旨と合致しています。（モックレスポンス）"
            }
        ] if corners_info else []
    
    try:
        model = genai.GenerativeModel(settings.gemini_model)
        
        # プロンプト作成
        corners_text = "\n\n".join([
            f"ID: {c['id']}\n番組: {c['program_title']}\nコーナー: {c['corner_title']}\n説明: {c['description']}"
            for c in corners_info
        ])
        
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
        
        response = model.generate_content(prompt)
        
        # レスポンスをパース
        response_text = response.text.strip()
        # ```json ... ``` を削除
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        recommendations = json.loads(response_text.strip())
        return recommendations
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # エラー時はモックデータを返す
        return [
            {
                "corner_id": corners_info[0]["id"],
                "score": 0.75,
                "reason": f"自動解析中にエラーが発生しました。手動で選択してください。"
            }
        ] if corners_info else []


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
    
    # ユーザーの全コーナー情報を取得
    corners = analyze_crud.get_user_corners(db, user_id)
    
    if not corners:
        return {"memo_id": memo_id, "recommendations": [], "error": "No corners found"}
    
    # Gemini用のコーナー情報を整形
    corners_info = [
        {
            "id": corner.id,
            "program_id": program.id,
            "program_title": program.title,
            "corner_title": corner.title,
            "description": corner.description_for_llm,
        }
        for corner, program in corners
    ]
    
    # Gemini APIで解析
    llm_recommendations = analyze_memo_with_gemini(memo.content, corners_info)
    
    # レスポンス形式に変換
    recommendations = []
    for rec in llm_recommendations:
        corner_info = next(
            (c for c in corners_info if c["id"] == rec["corner_id"]),
            None
        )
        if corner_info:
            recommendations.append({
                "corner_id": rec["corner_id"],
                "corner_title": corner_info["corner_title"],
                "program_id": corner_info["program_id"],
                "program_title": corner_info["program_title"],
                "score": rec["score"],
                "reason": rec["reason"],
            })
    
    return {
        "memo_id": memo.id,
        "recommendations": recommendations,
    }
