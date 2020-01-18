import enum
import functools
import typing
import uuid

from word_way.models import Pronunciation, Sentence, Word, WordRelation


@functools.singledispatch
def serialize(d, **options) -> dict:
    return {}


@serialize.register(dict)
def serialize_dict(d, **options) -> dict:
    return {k: serialize(v, **options) for k, v in d.items()}


@serialize.register(str)
@serialize.register(bool)
@serialize.register(int)
@serialize.register(float)
@serialize.register(type(None))
def serialize_literal(v, **options):
    return v


@serialize.register(list)
@serialize.register(set)
def serialize_list(l: typing.Iterable, **options) -> list:
    return [serialize(v, **options) for v in l]


@serialize.register(uuid.UUID)
def serialize_uuid(v: uuid.UUID, **options) -> str:
    return str(v)


@serialize.register(enum.Enum)
def serialize_enum(v: enum.Enum, **options):
    return serialize(v.value, **options)


@serialize.register(Pronunciation)
def serialize_pronunciation(v: Pronunciation, **options):
    return serialize(
        {
            'id': v.id,
            'pronunciation': v.pronunciation,
        },
        **options,
    )


@serialize.register(Word)
def serialize_word(v: Word, **options):
    return serialize(
        {
            'id': v.id,
            'target_code': v.target_code,
            'part': v.part,
            'contents': v.contents,
            'pronunciation_id': v.pronunciation_id,
        },
        **options,
    )


@serialize.register(Sentence)
def serialize_sentence(v: Sentence, **options):
    return serialize(
        {
            'id': v.id,
            'sentence': v.sentence,
        },
        **options,
    )


@serialize.register(WordRelation)
def serialize_word_relation(v: WordRelation, **options):
    return serialize(
        {
            'id': v.id,
            'word_id': v.word_id,
            'relation_word_id': v.relation_word_id,
            'relation_pronunciation_id': v.relation_pronunciation_id,
            'type': v.type,
        },
        **options,
    )
