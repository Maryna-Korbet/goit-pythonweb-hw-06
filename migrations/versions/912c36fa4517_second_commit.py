"""Second commit

Revision ID: 912c36fa4517
Revises: 8a212a9599ad
Create Date: 2025-04-10 18:20:25.711203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '912c36fa4517'
down_revision: Union[str, None] = '8a212a9599ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('students', 'group_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('subjects', 'teacher_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subjects', 'teacher_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('students', 'group_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
