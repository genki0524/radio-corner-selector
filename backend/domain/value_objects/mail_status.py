"""
バリューオブジェクト: メールステータス
"""
from enum import Enum


class MailStatus(str, Enum):
    """メールステータスの列挙型"""
    DRAFT = "下書き"
    SENT = "送信済み"
    ACCEPTED = "採用"
    REJECTED = "不採用"
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        """ステータスが有効かチェック"""
        return status in [s.value for s in cls]
    
    @classmethod
    def from_string(cls, status: str) -> "MailStatus":
        """文字列からMailStatusを生成"""
        for s in cls:
            if s.value == status:
                return s
        raise ValueError(f"Invalid mail status: {status}")
    
    def can_transition_to(self, new_status: "MailStatus") -> bool:
        """ステータス遷移が可能かチェック"""
        # 下書き → 送信済み → 採用/不採用
        transitions = {
            self.DRAFT: [self.SENT],
            self.SENT: [self.ACCEPTED, self.REJECTED],
            self.ACCEPTED: [],
            self.REJECTED: [],
        }
        return new_status in transitions.get(self, [])
