"""Initialize all of tables

Revision ID: 94abc68d90ce
Revises:
Create Date: 2020-03-21 16:20:10.994483

"""
from alembic import op
from sqlalchemy import (
    Column, Enum, ForeignKeyConstraint, Integer,
    PrimaryKeyConstraint, Unicode, UniqueConstraint,
)
from sqlalchemy_utils import UUIDType

revision = '94abc68d90ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pronunciation',
        Column('id', UUIDType, nullable=False),
        Column('pronunciation', Unicode(), nullable=False),
        PrimaryKeyConstraint('id'),
        UniqueConstraint('pronunciation'),
    )
    op.create_table(
        'sentence',
        Column('id', UUIDType, nullable=False),
        Column('sentence', Unicode(), nullable=False),
        PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'word_relation',
        Column('id', UUIDType, nullable=False),
        Column(
            'type',
            Enum('synonyms', 'include', name='word_relation_type'),
            nullable=False,
        ),
        PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'synonyms_word_relation',
        Column('id', UUIDType, nullable=False),
        Column('pronunciation_id', UUIDType, nullable=True),
        Column('related_pronunciation_id', UUIDType, nullable=True),
        ForeignKeyConstraint(['id'], ['word_relation.id'], ),
        ForeignKeyConstraint(['pronunciation_id'], ['pronunciation.id'], ),
        ForeignKeyConstraint(
            ['related_pronunciation_id'], ['pronunciation.id'],
        ),
        PrimaryKeyConstraint('id'),
        UniqueConstraint(
            'pronunciation_id',
            'related_pronunciation_id',
            name='uq_criteria_and_related_for_synonyms_relation',
        ),
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
        ForeignKeyConstraint(['pronunciation_id'], ['pronunciation.id'], ),
        PrimaryKeyConstraint('id'),
        UniqueConstraint('target_code'),
    )

    op.create_table(
        'include_word_relation',
        Column('id', UUIDType, nullable=False),
        Column('word_id', UUIDType, nullable=True),
        Column('related_pronunciation_id', UUIDType, nullable=True),
        ForeignKeyConstraint(['id'], ['word_relation.id'], ),
        ForeignKeyConstraint(
            ['related_pronunciation_id'], ['pronunciation.id'],
        ),
        ForeignKeyConstraint(['word_id'], ['word.id'], ),
        PrimaryKeyConstraint('id'),
        UniqueConstraint(
            'word_id',
            'related_pronunciation_id',
            name='uq_criteria_and_related_for_included_relation',
        )
    )

    op.create_table(
        'word_sentence_assoc',
        Column('word_id', UUIDType, nullable=False),
        Column('sentence_id', UUIDType, nullable=False),
        ForeignKeyConstraint(['sentence_id'], ['sentence.id'], ),
        ForeignKeyConstraint(['word_id'], ['word.id'], ),
        PrimaryKeyConstraint('word_id', 'sentence_id')
    )


def downgrade():
    op.drop_table('word_sentence_assoc')
    op.drop_table('include_word_relation')
    op.drop_table('word')
    op.drop_table('synonyms_word_relation')
    op.drop_table('word_relation')
    op.drop_table('sentence')
    op.drop_table('pronunciation')
