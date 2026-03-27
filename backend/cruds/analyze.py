"""
解析用のCRUD操作
"""
from typing import List, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session

from models import Memo, Program, Corner



def get_memo_by_id(db: Session, memo_id: int) -> Memo:
    """メモを取得"""
    return db.query(Memo).filter(Memo.id == memo_id).first()


def get_user_corners(db: Session, user_id: int) -> List[Tuple[Corner, Program]]:
    """ユーザーの全コーナー情報を取得"""
    return (
        db.query(Corner, Program)
        .join(Program)
        .filter(Program.user_id == user_id)
        .all()
    )


def search_corners_by_embedding(
    db: Session, embedding: List[float], threshold: float, limit: int
) -> list:
    """ベクトル検索でコーナーを取得"""
    # SQL = text("""
    # SELECT id, program_id, title, description_for_llm, similarity
    # FROM (
    #     SELECT id, program_id, title, description_for_llm,
    #            (1 - (embedded_description <=> :embedding)) AS similarity
    #     FROM corners
    # ) sub
    # WHERE similarity > :threshold
    # ORDER BY similarity DESC
    # LIMIT :limit
    # """)
    SQL = text("""
    SELECT id, program_id, title, description_for_llm, similarity
    FROM (
        SELECT id, program_id, title, description_for_llm,
               (1 - (embedded_description <=> :embedding)) AS similarity
        FROM corners
    ) sub
    ORDER BY similarity DESC
    LIMIT :limit
    """)
    result = db.execute(SQL, {"embedding": str(embedding), "threshold": threshold, "limit": limit})

    return result.fetchall()
