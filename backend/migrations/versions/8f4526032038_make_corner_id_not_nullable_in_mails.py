"""make_corner_id_not_nullable_in_mails

Revision ID: 8f4526032038
Revises: 34a87ab8dcf8
Create Date: 2026-01-28 21:56:52.045771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f4526032038'
down_revision: Union[str, Sequence[str], None] = '34a87ab8dcf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # corner_idがNULLのレコードがある場合は、まずそれらを削除するか適切な値を設定する必要があります
    # ここではNULLのレコードを持つ場合エラーになるため、事前にデータクレンジングが必要です
    op.alter_column('mails', 'corner_id',
               existing_type=sa.INTEGER(),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('mails', 'corner_id',
               existing_type=sa.INTEGER(),
               nullable=True)
