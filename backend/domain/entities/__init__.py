"""
ドメインエンティティ
ビジネスロジックを持つリッチなドメインオブジェクト
"""
from .memo_entity import MemoEntity
from .mail_entity import MailEntity
from .corner_entity import CornerEntity
from .program_entity import ProgramEntity

__all__ = [
    "MemoEntity",
    "MailEntity",
    "CornerEntity",
    "ProgramEntity",
]
