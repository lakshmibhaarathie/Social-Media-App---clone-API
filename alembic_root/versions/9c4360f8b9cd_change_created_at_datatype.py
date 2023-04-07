"""change created at datatype

Revision ID: 9c4360f8b9cd
Revises: 5b241044d9b0
Create Date: 2023-04-07 11:41:36.272192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c4360f8b9cd'
down_revision = '5b241044d9b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column(table_name="posts"
                    , column_name="created_at")


def downgrade() -> None:
    pass
