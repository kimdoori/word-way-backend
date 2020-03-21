import enum

__all__ = 'WordPart', 'WordRelationType',


class WordPart(enum.Enum):
    """
    단어의 품사를 정의합니다.

    FIXME: 관형사가 추가되어야 합니다.
    FIXME: 품사를 한글로 변경해야 합니다.
    """

    #: (:class:`str`) 명사
    noun = 'noun'

    #: (:class:`str`) 대명사
    pronoun = 'pronoun'

    #: (:class:`str`) 수사
    numeral = 'numeral'

    #: (:class:`str`) 조사
    postposition = 'postposition'

    #: (:class:`str`) 동사
    verb = 'verb'

    #: (:class:`str`) 형용사
    adjective = 'adjective'

    #: (:class:`str`) 부사
    adverb = 'adverb'

    #: (:class:`str`) 감탄사
    interjection = 'interjection'

    #: (:class:`str`) 알수없음
    unknown = 'unknown'


class WordRelationType(enum.Enum):
    """단어와 단어의 관계를 나타내는 종류입니다."""

    #: (:class:`str`) 동의어
    #: 의미가 비슷한 단어간의 관계
    synonyms = 'synonyms'

    #: (:class:`str`) 포함어
    #: 의미에 포함된 단어 관계
    include = 'include'
