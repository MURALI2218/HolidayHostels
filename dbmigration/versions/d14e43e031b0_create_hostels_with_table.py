"""create hostels with table

Revision ID: d14e43e031b0
Revises: 
Create Date: 2026-08-17 14:46:59.682902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd14e43e031b0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
def upgrade() -> None:
    op.create_table(
        "hostels",
        sa.Column("hostelid", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("hostelname", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("urgentrecruitment", sa.Boolean(), nullable=True),
        sa.Column("allowanceperday", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        # sa.Column("user_id", sa.Integer(), nullable=False),
        # sa.ForeignKeyConstraint(
        #     ["user_id"],
        #     ["users.userid"],
        #     ondelete="CASCADE",
        # ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
