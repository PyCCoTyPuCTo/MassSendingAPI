"""empty message

Revision ID: 2ce869ffbffd
Revises: 08f4711a7745
Create Date: 2024-06-13 10:36:41.952223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ce869ffbffd'
down_revision: Union[str, None] = '08f4711a7745'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO socialnetworks VALUES (1, 'Email')")
    op.execute("INSERT INTO socialnetworks VALUES (2, 'Telegram')")

def downgrade() -> None:
    op.execute("DELETE FROM socialnetworks")
