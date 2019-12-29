"""Initialize all of tables

Revision ID: e468a72af1b9
Revises:
Create Date: 2019-11-14 00:41:46.905677

"""
from alembic import op


from sqlalchemy import (
    Column, Enum, ForeignKeyConstraint, Integer, PrimaryKeyConstraint,
    Unicode, UniqueConstraint,
)
from sqlalchemy_utils import UUIDType


# revision identifiers, used by Alembic.

revision = 'e468a72af1b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pronunciation',
        Column('id', UUIDType, nullable=False),
        Column('pronunciation', Unicode(), nullable=False),
        PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'sentence',
        Column('id', UUIDType, nullable=False),
        Column('sentence', Unicode(), nullable=False),
        PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'word',
        Column('id', UUIDType, nullable=False),
        Column('target_code', Integer(), nullable=True),
        Column(
            'part',
            Enum(
                'noun',
                'pronoun',
                'numeral',
                'postposition',
                'verb',
                'adjective',
                'adverb',
                'interjection',
                'unknown',
                name='word_part'
            ),
            nullable=False,
        ),
        Column('contents', Unicode(), nullable=False),
        Column('pronunciation_id', UUIDType, nullable=False),
        ForeignKeyConstraint(['pronunciation_id'], ['pronunciation.id']),
        PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'word_relation',
        Column('id', UUIDType, nullable=False),
        Column('word_id', UUIDType, nullable=True),
        Column('relation_word_id', UUIDType, nullable=True),
        Column('relation_pronunciation_id', UUIDType, nullable=True),
        Column(
            'type',
            Enum('synonyms', name='word_relation_type'),
            nullable=False
        ),
        ForeignKeyConstraint(
            ['relation_pronunciation_id'],
            ['pronunciation.id'],
        ),
        ForeignKeyConstraint(
            ['relation_word_id'],
            ['word.id'],
        ),
        ForeignKeyConstraint(
            ['word_id'],
            ['word.id'],
        ),
        PrimaryKeyConstraint('id'),
        UniqueConstraint(
            'word_id',
            'relation_word_id',
            'relation_pronunciation_id',
            name='uq_word_relation_word_and_pronunciation'
        )
    )

    op.create_table(
        'word_sentence_assoc',
        Column('word_id', UUIDType, nullable=False),
        Column('sentence_id', UUIDType, nullable=False),
        ForeignKeyConstraint(['sentence_id'], ['sentence.id']),
        ForeignKeyConstraint(['word_id'], ['word.id']),
        PrimaryKeyConstraint('word_id', 'sentence_id'),
    )


def downgrade():
    op.drop_table('word_sentence_assoc')
    op.drop_table('word_relation')
    op.drop_table('word')
    op.drop_table('sentence')
    op.drop_table('pronunciation')
