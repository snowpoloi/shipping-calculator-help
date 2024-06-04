"""empty message

Revision ID: a20b04fd1eaf
Revises: 156e81b42dcc
Create Date: 2024-06-03 00:37:15.619366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a20b04fd1eaf'
down_revision = '156e81b42dcc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offer_postal_code',
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.Column('postal_code_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ),
    sa.ForeignKeyConstraint(['postal_code_id'], ['postal_code.id'], ),
    sa.PrimaryKeyConstraint('offer_id', 'postal_code_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('offer_postal_code')
    # ### end Alembic commands ###
