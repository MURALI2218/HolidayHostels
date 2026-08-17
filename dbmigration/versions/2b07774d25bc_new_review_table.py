"""New Review Table

Revision ID: 2b07774d25bc
Revises: 9a50d832bf43
Create Date: 2026-08-17 22:42:44.483735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b07774d25bc'
down_revision: Union[str, Sequence[str], None] = '9a50d832bf43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table(
            "reviews",
            sa.Column("user_id",sa.Integer(),nullable=False),
            sa.Column("hostel_id", sa.Integer(), nullable=False),
            sa.Column("hostel_review", sa.String(), nullable=False),
            )
     sa.PrimaryKeyConstraint("user_id", "hostel_id")
     op.create_foreign_key(
                    "fk_reviews_user_id_users",
                    "reviews",
                    "users",
                    ["user_id"],
                    ["userid"],
                    ondelete="CASCADE"
                ),
     op.create_foreign_key(
                 'fk_reviews_hostel_id',
                 'reviews',
                 "hostels",
                 ["hostel_id"],
                 ["hostelid"],
                 ondelete="CASCADE"
            )

            


def downgrade() -> None:
    
    
    op.drop_constraint(
        "fk_reviews_hostel_id_hostels",
        "reviews",
        type_="foreignkey"
    )

    op.drop_constraint(
        "fk_reviews_user_id_users",
        "reviews",
        type_="foreignkey"
    )

    op.drop_table("reviews")
