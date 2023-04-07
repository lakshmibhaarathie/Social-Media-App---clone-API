"""create posts table

Revision ID: fc9193140c06
Revises: 
Create Date: 2023-04-07 11:25:05.184250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc9193140c06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column(name="id", type_=sa.Integer, nullable=False)
                    , sa.Column(name="title", type_=sa.String, nullable=False)
                    , sa.Column(name="content", type_=sa.String, nullable=False)
    )


def downgrade() -> None:
    pass
