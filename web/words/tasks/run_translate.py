"""Translates words from db."""

from celery import shared_task
from loguru import logger
from translate import Translator
from words.models import Language, Translation, Word


@shared_task
def run_translate(word_id: int, target_lang: str) -> None:
    """Stupid function that translates words."""
    logger.info('start')
    word = Word.objects.all().select_related('lang').get(id=word_id)
    source_l, target_l = word.lang, Language.objects.get(code=target_lang)
    translator = Translator(from_lang=source_l.code, to_lang=target_l.code)
    logger.debug('handle: {}', word.content)

    translation = translator.translate(word.content)
    translation = Word.objects.create(content=translation, lang=ru)
    Translation.objects.create(one=word, other=translation)
    logger.info(
        'Translated: "{}" => "{}"',
        word.content, translation.content,
    )
