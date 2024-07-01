"""empty message

Revision ID: fc09d72a99d6
Revises: 2166292a287c
Create Date: 2024-07-01 17:27:15.649873

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fc09d72a99d6'
down_revision = '2166292a287c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.alter_column('fcm_message_id',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=150),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.alter_column('fcm_message_id',
               existing_type=sa.String(length=150),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###