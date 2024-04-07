"""create sub_bills table

Revision ID: 61eac20627c2
Revises: 1c846c4e5452
Create Date: 2024-04-06 11:58:07.787616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61eac20627c2'
down_revision: Union[str, None] = '1c846c4e5452'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "sub_bills",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column("reference", sa.String, nullable=True),
        sa.Column("bill_id", sa.Integer, sa.ForeignKey("bills.id"), nullable=False),
    )


def downgrade():
    op.drop_table("sub_bills")
