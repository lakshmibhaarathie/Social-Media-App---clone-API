"""change created at datatype

Revision ID: d40c23b67e52
Revises: 9c4360f8b9cd
Create Date: 2023-04-07 11:46:36.651572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd40c23b67e52'
down_revision = '9c4360f8b9cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(table_name="posts"
                  , column=sa.Column(name="created_at"
                                    , type_=sa.TIMESTAMP(timezone=True)
                                    , server_default=sa.text('now()')
                                    , nullable=False)
    )


def downgrade() -> None:
    op.drop_column(table_name="posts", column_name="created_at")
