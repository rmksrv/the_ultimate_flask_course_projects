"""empty message

Revision ID: a8267f67b9cb
Revises: e9728c3c8a62
Create Date: 2022-11-07 23:23:31.190277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a8267f67b9cb"
down_revision = "e9728c3c8a62"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("joined_at", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "joined_at")
    # ### end Alembic commands ###
