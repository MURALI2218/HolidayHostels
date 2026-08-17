"""create users

Revision ID: 237e189807de
Revises: d14e43e031b0
Create Date: 2026-08-17 15:05:03.869335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '237e189807de'
down_revision: Union[str, Sequence[str], None] = 'd14e43e031b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "userid",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),
        sa.Column(
            "username",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "emailid",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "password",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.UniqueConstraint("emailid")
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
