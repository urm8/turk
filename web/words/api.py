from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Schema, router
from ninja.errors import HttpError
from words.models import Example, Language, Translation, Word

_ = words_router = router.Router()


class WordIn(Schema):
    content: str
    lang_id: str


class WordOut(WordIn):
    id: int


@_.post('/', response=WordOut)
def add_word(_, payload: WordIn) -> Word:
    return Word.objects.create(**payload.dict())


@_.post('/{word_id}/', response=WordOut)
def read_word(_, word_id: int) -> Word:
    return get_object_or_404(Word, id=word_id)


@_.get('/{lang}/search', response=list[WordOut])
def search_word(_, lang: str, q: str):
    return Word.objects.filter(lang_id=lang, content__icontains=q)[:10]


class TranslationIn(Schema):
    content: str


class TranslationOut(TranslationIn):
    id: int
    language_id: str


@_.post('/{word_id}/{language_code}/', response=TranslationOut)
def add_translation(_, word_id: int, language_code: str, payload: TranslationIn) -> Translation:
    if not Language.objects.filter(code=language_code).exists():
        raise HttpError(400, f'unknown language code: {language_code}')
    try:
        return Translation.objects.create(**payload.dict(), word_id=word_id, lang_id=language_code)
    except IntegrityError:
        raise HttpError(400, f'word: {word_id} not found.')


@_.get('/{word_id}/{language_code}/')
def get_examples(_, word_id: int, language_code: str) -> list[Example]:
    return Example.objects.filter(word_id=word_id, lang_id=language_code)[:10]
