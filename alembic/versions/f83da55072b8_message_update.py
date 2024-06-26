"""message_update

Revision ID: f83da55072b8
Revises: a987cf8b7fbe
Create Date: 2024-06-24 10:38:00.288813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f83da55072b8'
down_revision: Union[str, None] = 'a987cf8b7fbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('text', sa.String(), nullable=True))
    op.drop_column('message', 'message')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('message', 'text')
    # ### end Alembic commands ###
