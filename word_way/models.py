import uuid

from sqlalchemy import Column, ForeignKey, Integer, Unicode, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_enum34 import EnumType
from sqlalchemy_utils.types.uuid import UUIDType

from .enum import WordPart, WordRelationType
from .orm import Base


__all__ = (
    'Word', 'Sentence', 'WordSentenceAssoc', 'Pronunciation', 'WordRelation',
)


class Pronunciation(Base):
    """
    단어의 소리를 나타내는 테이블.
    유사어 데이터를 가지고 올 때에는 특정 단어 id가 아닌 발음밖에 가져오지 못하므로
    (:class:`Word`) 와 분리 해야 합니다.
    """

    #: (:class:`uuid.UUID`) 고유 식별자.
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)

    #: (:class:`str`) 발음
    pronunciation = Column(Unicode, nullable=False)

    __tablename__ = 'pronunciation'


class Word(Base):
    """단어에 대한 정보를 저장하는 테이블"""

    #: (:class:`uuid.UUID`) 고유 식별자.
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)

    #: (:class:`int`) 우리말샘 API 에서 사용되는 고유 식별자.
    target_code = Column(Integer)

    #: (:class:`WordPart`) 단어의 품사
    part = Column(EnumType(WordPart, name='word_part'), nullable=False)

    #: (:class:`str`) 단어의 의미
    contents = Column(Unicode, nullable=False)

    #: (:class:`uuid.UUID`) 발음에 대한 고유 식별자.
    pronunciation_id = Column(
        UUIDType, ForeignKey(Pronunciation.id), nullable=False,
    )

    #: (:class:`Pronunciation`) 발음
    pronunciation = relationship(Pronunciation, uselist=False)

    __tablename__ = 'word'


class Sentence(Base):
    """문장을 저장하는 테이블. 예문을 위해 나타내기 위해 존재합니다."""

    #: (:class:`uuid.UUID`) 고유 식별자.
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)

    #: (:class:`str`) 문장
    sentence = Column(Unicode, nullable=False)

    __tablename__ = 'sentence'


class WordSentenceAssoc(Base):
    """
    단어와 문장의 관계를 나타내는 테이블.
    하나의 문장이 여러 단어의 예문이 될 수 있으므로 (다대다 관계) Assoc 테이블로 관리합니다.
    """
    #: (:class:`uuid.UUID`) 단어에 대한 고유 식별자.
    word_id = Column(UUIDType, ForeignKey(Word.id), primary_key=True)

    #: (:class:`Word`) 단어
    word = relationship(Word)

    #: (:class:`uuid.UUID`) 예문에 대한 고유 식별자.
    sentence_id = Column(UUIDType, ForeignKey(Sentence.id), primary_key=True)

    #: (:class:`Sentence`) 예문
    sentence = relationship(Sentence)

    __tablename__ = 'word_sentence_assoc'


class WordRelation(Base):
    """
    단어간의 관계를 나타내는 테이블.

    `사랑`이라는 단어와 `애정`이라는 단어가 서로 유의어 관계일 경우,
    `word_id`에는 `사랑`의 id가, `relation_word_id`에는 `애정`의 id가 들어가게 되며,
    이때 `type`은 `synonyms`이 들어가게 됩니다.

    """
    #: (:class:`uuid.UUID`) 고유 식별자.
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)

    #: (:class:`uuid.UUID`) 단어 고유 식별자.
    word_id = Column(UUIDType, ForeignKey(Word.id))

    #: (:class:`uuid.UUID`) 관련된 단어 식별자.
    relation_word_id = Column(UUIDType, ForeignKey(Word.id), nullable=True)

    #: (:class:`uuid.UUID`) 관련된 발음 식별자.
    relation_pronunciation_id = Column(
        UUIDType, ForeignKey(Pronunciation.id), nullable=True,
    )

    #: (:class:`WordRelationType`) 단어간의 관계 종류
    type = Column(
        EnumType(WordRelationType, name='word_relation_type'),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            'word_id',
            'relation_word_id',
            'relation_pronunciation_id',
            name='uq_word_relation_word_and_pronunciation',
        ),
    )
    __tablename__ = 'word_relation'
