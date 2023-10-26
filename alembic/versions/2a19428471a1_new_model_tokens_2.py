"""new model Tokens 2

Revision ID: 2a19428471a1
Revises: edfb36e4282a
Create Date: 2023-10-25 19:02:24.085204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a19428471a1'
down_revision = 'edfb36e4282a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver', sa.BigInteger(), nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('last_used', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['driver'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens')
    # ### end Alembic commands ###