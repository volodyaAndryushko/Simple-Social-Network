"""add user table

Revision ID: f7f85e1bcbb2
Revises: 
Create Date: 2023-03-27 17:04:14.776484

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7f85e1bcbb2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("password_salt", sa.String(30), nullable=False),
        sa.Column("password_hash", sa.Text, nullable=False),
        sa.Column("created_time", sa.DateTime, default=datetime.utcnow),
        sa.Column("last_login_time", sa.DateTime),
        sa.Column("last_request_time", sa.DateTime),
    )


def downgrade():
    op.drop_table("user")
