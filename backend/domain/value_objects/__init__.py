"""
バリューオブジェクト
不変で値による等価性を持つオブジェクト
"""
from .mail_status import MailStatus
from .email_address import EmailAddress
from .recommendation_score import RecommendationScore

__all__ = [
    "MailStatus",
    "EmailAddress",
    "RecommendationScore",
]
