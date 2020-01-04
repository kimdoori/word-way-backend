""":mod:`word_way.word_data` --- 단어 정보 저장(DB)과 관련된 API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import typing
import xml.etree.ElementTree as elemTree

from flask import Blueprint, abort, jsonify, request
from requests import get as requests_get
from urllib.parse import urljoin

from .config import get_word_api_config
from .context import session
from .models import Pronunciation, Sentence, Word, WordSentenceAssoc
from .utils import convert_word_part

__all__ = 'word_data', 'save_word_data',


word_data = Blueprint('word_data', __name__, url_prefix='/word_data')


@word_data.route('/', methods=['POST'])
def save_word_data():
    '''우리말샘 API로 단어 정보를 가져와서 DB에 저장하는 API'''
    params = request.get_json()
    target_word = params.get('word')

    # 단어 기본 정보 요청
    config = get_word_api_config()
    params = {
        'key': config.get('token'),
        'q': target_word,
        'target_type': 'search',
        'part': 'word',
        'sort': 'dict',
    }
    url = urljoin(config.get('url'), 'search')
    res = requests_get(url, params=params)
    res.raise_for_status()

    res_tree = elemTree.fromstring(res.text)
    words = save_word(target_word, res_tree)
    if not words:
        abort(404)

    return jsonify(success=True)


def save_word(
    target_word: str,
    tree: elemTree.ElementTree
) -> typing.Sequence[Word]:
    '''단어 정보를 DB에 저장합니다.'''

    pronunciation = session.query(Pronunciation).filter(
        Pronunciation.pronunciation == target_word
    ).one_or_none()
    if not pronunciation:
        pronunciation = Pronunciation(pronunciation=target_word)
        session.add(pronunciation)
        session.commit()

    words = []

    for item in tree.findall('item'):
        for sense in item.findall('sense'):
            target_code = sense.findtext('target_code')
            word = Word(
                target_code=int(target_code),
                part=convert_word_part(sense.findtext('pos')),
                contents=sense.findtext('definition'),
                pronunciation_id=pronunciation.id,
            )
            session.add(word)
            session.commit()
            save_extra_info(word)
            words.append(word)

    return words


def save_extra_info(word: Word):
    '''단어의 예문과 유의어를 가져와 저장합니다.'''
    # 단어 추가 정보 요청
    config = get_word_api_config()
    params = {
        'key': config.get('token'),
        'q': word.target_code,
        'target_type': 'view',
        'method': 'target_code',
    }
    url = urljoin(config.get('url'), 'view')
    res = requests_get(url, params=params)
    res.raise_for_status()

    tree = elemTree.fromstring(res.text)
    sense_info = tree.find('item').find('senseInfo')

    # TODO: 유의어 정보도 저장해야합니다.

    for example_info in sense_info.findall('example_info'):
        sentence = Sentence(sentence=example_info.findtext('example'))
        session.add(sentence)
        session.commit()
        assoc = WordSentenceAssoc(word_id=word.id, sentence_id=sentence.id)
        session.add(assoc)
    session.commit()
