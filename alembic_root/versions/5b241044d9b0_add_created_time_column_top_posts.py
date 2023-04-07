"""add created time column top posts

Revision ID: 5b241044d9b0
Revises: fc9193140c06
Create Date: 2023-04-07 11:33:05.744296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b241044d9b0'
down_revision = 'fc9193140c06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(table_name="posts", column=sa.Column(name="created_at", type_=sa.Integer, nullable=False))
    op.create_primary_key(constraint_name="primary_key_post_id", table_name="posts", columns=["id"])

def downgrade() -> None:
    op.drop_column(table_name="posts",column_name="created_at")
    op.drop_constraint(constraint_name="primary_key_post_id", table_name="posts")
