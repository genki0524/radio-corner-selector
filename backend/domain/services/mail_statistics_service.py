"""
ドメインサービス: メール統計
メール関連の統計処理
"""
from typing import List
from domain.entities.mail_entity import MailEntity
from domain.value_objects.mail_status import MailStatus


class MailStatisticsService:
    """メール統計に関するドメインサービス"""
    
    @staticmethod
    def calculate_statistics(mails: List[MailEntity]) -> dict:
        """
        メール統計を計算
        
        Args:
            mails: メールエンティティのリスト
        
        Returns:
            統計情報の辞書
        """
        total = len(mails)
        draft = sum(1 for m in mails if m.status == MailStatus.DRAFT)
        sent = sum(1 for m in mails if m.status == MailStatus.SENT)
        accepted = sum(1 for m in mails if m.status == MailStatus.ACCEPTED)
        rejected = sum(1 for m in mails if m.status == MailStatus.REJECTED)
        
        return {
            "total": total,
            "draft": draft,
            "sent": sent,
            "accepted": accepted,
            "rejected": rejected
        }
    
    @staticmethod
    def calculate_acceptance_rate(mails: List[MailEntity]) -> float:
        """
        採用率を計算
        
        Args:
            mails: メールエンティティのリスト
        
        Returns:
            採用率（0.0-1.0）
        """
        sent_or_finished = [
            m for m in mails
            if m.status in [MailStatus.SENT, MailStatus.ACCEPTED, MailStatus.REJECTED]
        ]
        
        if not sent_or_finished:
            return 0.0
        
        accepted = sum(1 for m in sent_or_finished if m.status == MailStatus.ACCEPTED)
        return accepted / len(sent_or_finished)
    
    @staticmethod
    def get_most_active_corner(mails: List[MailEntity]) -> tuple[int, int]:
        """
        最も投稿の多いコーナーを取得
        
        Args:
            mails: メールエンティティのリスト
        
        Returns:
            (コーナーID, 投稿数) のタプル
        """
        if not mails:
            return (0, 0)
        
        corner_counts = {}
        for mail in mails:
            corner_counts[mail.corner_id] = corner_counts.get(mail.corner_id, 0) + 1
        
        max_corner = max(corner_counts.items(), key=lambda x: x[1])
        return max_corner
