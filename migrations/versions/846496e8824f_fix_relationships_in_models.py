"""Fix relationships in models

Revision ID: 846496e8824f
Revises: 94d645e0bdb8
Create Date: 2024-06-03 22:37:11.896964

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '846496e8824f'
down_revision = '94d645e0bdb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company_postal_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('postal_code_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('accessible', 'hard_to_reach', 'not_serviced'), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['postal_code_id'], ['postal_code.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('offer', schema=None) as batch_op:
        batch_op.alter_column('base_cost',
               existing_type=mysql.FLOAT(),
               nullable=False)

    with op.batch_alter_table('postal_code', schema=None) as batch_op:
        batch_op.alter_column('postal_code',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=20),
               existing_nullable=False)
        batch_op.alter_column('area_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
        batch_op.alter_column('prefecture',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('postal_code', schema=None) as batch_op:
        batch_op.alter_column('prefecture',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
        batch_op.alter_column('area_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
        batch_op.alter_column('postal_code',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=10),
               existing_nullable=False)

    with op.batch_alter_table('offer', schema=None) as batch_op:
        batch_op.alter_column('base_cost',
               existing_type=mysql.FLOAT(),
               nullable=True)

    op.drop_table('company_postal_code')
    # ### end Alembic commands ###