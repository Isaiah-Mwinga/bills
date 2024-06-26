"""create bills table

Revision ID: 1c846c4e5452
Revises: 
Create Date: 2024-04-05 18:57:30.786033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c846c4e5452'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "bills",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("total", sa.Float, nullable=False),
        sa.Column("sub_bills", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("bills")
