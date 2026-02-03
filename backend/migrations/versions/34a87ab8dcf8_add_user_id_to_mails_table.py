"""add_user_id_to_mails_table

Revision ID: 34a87ab8dcf8
Revises: e0346440e332
Create Date: 2026-01-28 20:18:27.540043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34a87ab8dcf8'
down_revision: Union[str, Sequence[str], None] = 'e0346440e332'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add user_id column to mails table
    op.add_column('mails', sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Populate user_id from corner -> program -> user relationship
    # Only for records where corner_id is not null
    op.execute("""
        UPDATE mails
        SET user_id = (
            SELECT programs.user_id
            FROM corners
            JOIN programs ON corners.program_id = programs.id
            WHERE corners.id = mails.corner_id
        )
        WHERE corner_id IS NOT NULL
    """)
    
    # For records where corner_id is null, try to get user_id from memo
    op.execute("""
        UPDATE mails
        SET user_id = (
            SELECT memos.user_id
            FROM memos
            WHERE memos.id = mails.memo_id
        )
        WHERE corner_id IS NULL AND memo_id IS NOT NULL AND user_id IS NULL
    """)
    
    # Delete any mails that still don't have a user_id (orphaned records)
    op.execute("DELETE FROM mails WHERE user_id IS NULL")
    
    # Make user_id NOT NULL after data migration
    op.alter_column('mails', 'user_id', nullable=False)
    
    # Create foreign key
    op.create_foreign_key('fk_mails_user_id', 'mails', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Remove user_id column
    op.drop_constraint('fk_mails_user_id', 'mails', type_='foreignkey')
    op.drop_column('mails', 'user_id')
