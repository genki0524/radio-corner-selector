"""
ドメインサービス: メール作成
複数エンティティにまたがるビジネスロジック
"""
from typing import Optional
from domain.entities.memo_entity import MemoEntity
from domain.entities.corner_entity import CornerEntity
from domain.entities.program_entity import ProgramEntity
from domain.value_objects.mail_status import MailStatus


class MailCreationService:
    """メール作成に関するドメインサービス"""
    
    @staticmethod
    def create_mail_draft_from_memo(
        memo: MemoEntity,
        corner: CornerEntity,
        program: ProgramEntity,
        custom_subject: Optional[str] = None
    ) -> dict:
        """
        メモからメール下書きを作成
        
        Args:
            memo: メモエンティティ
            corner: コーナーエンティティ
            program: 番組エンティティ
            custom_subject: カスタム件名（任意）
        
        Returns:
            メール作成用のデータ辞書
        """
        # 件名を生成
        if custom_subject:
            subject = custom_subject
        else:
            subject = f"{program.title} - {corner.title}への投稿"
        
        # 本文を生成（メモの内容をベースに）
        body = memo.content
        
        return {
            "corner_id": corner.id,
            "memo_id": memo.id,
            "subject": subject,
            "body": body,
            "status": MailStatus.DRAFT.value
        }
    
    @staticmethod
    def validate_mail_submission(program: ProgramEntity) -> None:
        """
        メール送信可能かバリデーション
        
        Args:
            program: 番組エンティティ
        
        Raises:
            ValueError: 送信できない場合
        """
        if not program.can_submit_mail():
            raise ValueError(
                f"Program '{program.title}' does not have an email address configured"
            )
