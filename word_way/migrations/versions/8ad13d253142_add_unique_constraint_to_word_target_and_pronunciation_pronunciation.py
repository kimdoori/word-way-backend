"""add unique constraint to Word.target_code and Pronunciation.pronunciation

Revision ID: 8ad13d253142
Revises: e468a72af1b9
Create Date: 2020-01-04 16:51:05.964532

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '8ad13d253142'
down_revision = 'e468a72af1b9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'word', ['target_code'])
    op.create_unique_constraint(None, 'pronunciation', ['pronunciation'])


def downgrade():
    op.drop_constraint(None, 'word', type_='unique')
    op.drop_constraint(None, 'pronunciation', type_='unique')
