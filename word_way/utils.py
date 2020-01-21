from word_way.enum import WordPart


def convert_word_part(part: str):
    return {
        '명사': WordPart.noun,
        '대명사': WordPart.pronoun,
        '수사': WordPart.numeral,
        '조사': WordPart.postposition,
        '동사': WordPart.verb,
        '형용사': WordPart.adjective,
        '부사': WordPart.adverb,
        '감탄사': WordPart.interjection,
    }.get(part, WordPart.unknown)
