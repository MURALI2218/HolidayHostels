"""ADD COLUMN IN HOSTELS

Revision ID: 9a50d832bf43
Revises: 237e189807de
Create Date: 2026-08-17 15:27:39.735913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a50d832bf43'
down_revision: Union[str, Sequence[str], None] = '237e189807de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
       op.add_column(
        "hostels",
        sa.Column("user_id", sa.Integer(), nullable=False)
    )

       op.create_foreign_key(
        "fk_hostels_user_id_users",
        "hostels",
        "users",
        ["user_id"],
        ["userid"],
        ondelete="CASCADE"
    )
    
    

def downgrade() -> None:
    """Downgrade schema."""
    pass
