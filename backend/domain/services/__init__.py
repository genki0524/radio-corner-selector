"""
ドメインサービス
複数エンティティにまたがるビジネスロジック
"""
from .mail_creation_service import MailCreationService
from .corner_recommendation_service import CornerRecommendationService
from .mail_statistics_service import MailStatisticsService

__all__ = [
    "MailCreationService",
    "CornerRecommendationService",
    "MailStatisticsService",
]
