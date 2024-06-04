"""Update models with postal code relationships

Revision ID: d23ad87b7685
Revises: d8e669c12bd4
Create Date: 2024-06-03 23:07:40.843234

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd23ad87b7685'
down_revision = 'd8e669c12bd4'
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
    with op.batch_alter_table('postal_code', schema=None) as batch_op:
        batch_op.alter_column('area_name',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('prefecture',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('postal_code', schema=None) as batch_op:
        batch_op.alter_column('prefecture',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('area_name',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)

    op.drop_table('company_postal_code')
    # ### end Alembic commands ###
