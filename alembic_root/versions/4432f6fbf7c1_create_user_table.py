"""create user table

Revision ID: 4432f6fbf7c1
Revises: d40c23b67e52
Create Date: 2023-04-07 11:51:01.977825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4432f6fbf7c1'
down_revision = 'd40c23b67e52'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users" 
                    , sa.Column(name="id", type_=sa.Integer
                                , nullable=False, primary_key=True) 
                    , sa.Column(name="email", type_=sa.String
                                , nullable=False, unique=True)
                    , sa.Column(name="password", type_=sa.String
                                , nullable=False)
                    , sa.Column(name="created_at", type_=sa.TIMESTAMP(timezone=True)
                                , nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table(table_name="users")
