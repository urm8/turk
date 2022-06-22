from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from loguru import logger
from ninja import Field, Schema
from ninja.router import Router
from polls.models import Answer, PollStats, UserLanguage, UserWord
from polls.selectors import read_random_answer
from polls.service.user_language import set_user_language
from words.api import WordOut
from words.models import Translation, Word
from words.selectors import translation_exists, translation_exists_by_word

_ = polls_api = Router()


class AnswerOut(Schema):
    content: str


class UserLanguageIn(Schema):
    native_language_id: str = Field(..., alias='native_language')
    learn_language_id: str = Field(..., alias='learn_language')


class UserLanguageOut(UserLanguageIn):
    native_language_id: str
    learn_language_id: str
    user_id: int


class UserWordIn(Schema):
    word: str
    translation: str

    class Config:
        anystr_strip_whitespace = True
        anystr_lower = True


class PollStatsIn(Schema):
    correct: bool


class PollStats(Schema):
    user_id: int
    correct_answers: int
    total_answers: int


@_.get('/answer/{lang}/{answer_type}/', response=AnswerOut)
def read_answer(_, lang: str, answer_type: Answer.Type) -> Answer:
    return read_random_answer(lang, answer_type)


@_.get('/{user_id}/language/', response=UserLanguageOut)
def read_language(_, user_id: int) -> UserLanguage:
    return get_object_or_404(UserLanguage, user_id=user_id)


@_.post('/{user_id}/language/', response=UserLanguageOut)
def set_language(_, user_id: int, payload: UserLanguageIn) -> UserLanguage:
    return set_user_language(user_id, payload.native_language_id, payload.learn_language_id)


@_.post('/{user_id}/word/{lang_from}/{lang_to}', response=WordOut)
def add_word(_, user_id: int, lang_from: str, lang_to: str, payload: UserWordIn) -> Word:
    with atomic():
        word, word_created = Word.objects.get_or_create(
            content=payload.word, lang_id=lang_from,
        )

        if word_created:
            logger.info(f'added new word: {word}')

        translation_word, _ = Word.objects.get_or_create(
            content=payload.translation, lang_id=lang_to,
        )

        if _:
            logger.info(f'added new word: {translation_word}')

        if translation_exists_by_word(word, translation_word) is None:
            Translation.objects.create(one=word, other=translation_word)

        user_word, created = UserWord.objects.get_or_create(
            word=word, user_id=user_id,
        )
        if created:
            logger.info(f'assigned new word to {user_id}: {word}')
        return user_word.word


@_.put('/{user_id}/stats')
@atomic
def create_or_update_stats(_, user_id, payload: PollStatsIn):
    obj, _ = PollStats.objects.get_or_create(user_id=user_id)
    if payload.correct:
        obj.correct_answers += 1
    obj.total_attempts += 1
    obj.save()
    return obj
