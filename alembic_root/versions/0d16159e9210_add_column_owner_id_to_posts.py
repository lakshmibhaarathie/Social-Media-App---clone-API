"""add column owner_id to posts

Revision ID: 0d16159e9210
Revises: 4432f6fbf7c1
Create Date: 2023-04-07 12:12:31.244989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d16159e9210'
down_revision = '4432f6fbf7c1'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(table_name="posts", column=sa.Column(
        name="owner_id", type_=sa.Integer, nullable=False)
    )

    op.create_foreign_key(
        constraint_name="post_user_id", source_table="posts"
        , referent_table="users", local_cols=["owner_id"]
        , remote_cols=["id"], ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint(constraint_name="post_user_id", table_name="posts")
    op.drop_column(table_name="posts", column_name="owner_id")
