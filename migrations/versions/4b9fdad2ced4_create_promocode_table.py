"""create promocode table

Revision ID: 4b9fdad2ced4
Revises: 
Create Date: 2023-07-07 17:41:20.783423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b9fdad2ced4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promocode',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user', sa.String(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('promocode', sa.String(), nullable=False),
    sa.Column('issued_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('reason', sa.Enum('bug', 'event', 'other', name='reasontype'), nullable=True),
    sa.Column('ticket_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('promocode')
    # ### end Alembic commands ###
