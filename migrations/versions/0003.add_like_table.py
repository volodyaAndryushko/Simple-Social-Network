"""add like table

Revision ID: d99c6f96b916
Revises: 8c3dc1bd8910
Create Date: 2023-03-28 14:55:18.423795

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd99c6f96b916'
down_revision = '8c3dc1bd8910'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "like",
        sa.Column("post_id", sa.Integer, nullable=False),
        sa.Column("liked_by_id", sa.Integer, nullable=False),
        sa.Column("created_time", sa.DateTime, default=datetime.utcnow),
    )
    op.create_foreign_key("fk_like_liked_by", "like", "user", ["liked_by_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_like_post_id", "like", "post", ["post_id"], ["id"], ondelete="CASCADE")


def downgrade():
    op.drop_table("like")
