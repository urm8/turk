from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Schema, router
from ninja.errors import HttpError
from words.models import Language, Translation, Word

R = router.Router()


class WordIn(Schema):
    content: str


class WordOut(WordIn):
    id: int


@R.post('/', response=WordOut)
def add_word(_, payload: WordIn) -> Word:
    return Word.objects.create(**payload.dict())


@R.post('/{word_id}/', response=WordOut)
def read_word(_, word_id: int) -> Word:
    return get_object_or_404(Word, id=word_id)


class TranslationIn(Schema):
    content: str


class TranslationOut(TranslationIn):
    id: int
    language_id: str


@R.post('/{word_id}/{language_code}/', response=TranslationOut)
def add_translation(_, word_id: int, language_code: str, payload: TranslationIn) -> Translation:
    if not Language.objects.filter(code=language_code).exists():
        raise HttpError(400, f'unknown language code: {language_code}')
    try:
        return Translation.objects.create(**payload.dict(), word_id=word_id, lang_id=language_code)
    except IntegrityError:
        raise HttpError(400, f'word: {word_id} not found.')
