"""add post table

Revision ID: 8c3dc1bd8910
Revises: f7f85e1bcbb2
Create Date: 2023-03-27 22:24:24.753440

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c3dc1bd8910'
down_revision = 'f7f85e1bcbb2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "post",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("author_id", sa.Integer, nullable=False),
        sa.Column("title", sa.String(60), nullable=False),
        sa.Column("content", sa.Text),
        sa.Column("created_time", sa.DateTime, default=datetime.utcnow),
    )
    op.create_foreign_key("fk_post_author_id", "post", "user", ["author_id"], ["id"], ondelete="CASCADE")


def downgrade():
    op.drop_table("post")
