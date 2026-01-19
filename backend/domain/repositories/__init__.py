"""
リポジトリインターフェース
データアクセスの抽象化
"""
from .memo_repository import MemoRepositoryInterface
from .mail_repository import MailRepositoryInterface
from .corner_repository import CornerRepositoryInterface
from .program_repository import ProgramRepositoryInterface

__all__ = [
    "MemoRepositoryInterface",
    "MailRepositoryInterface",
    "CornerRepositoryInterface",
    "ProgramRepositoryInterface",
]
