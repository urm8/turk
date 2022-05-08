"""Translates words from db."""
import asyncio

from django.db.models import Exists, OuterRef, Q
from loguru import logger
from translate import Translator
from words.models import Language, Translation, Word


def translate():
    """Stupid function that translates words."""
    logger.info('start')
    translator = Translator(to_lang='ru', from_lang='tr')
    logger.debug('handle: {}')
    ru, tr = Language.objects.get(code='ru'), Language.objects.get(code='tr')
    for word in Word.objects.filter(lang=tr).exclude(
            Exists(
                Translation.objects.filter(
                    Q(one_id=OuterRef('id'), other__lang=ru) | Q(
                        other_id=OuterRef('id'), one__lang=ru,
                    ),
                ),
            ),
    ):
        translation = translator.translate(word.content)
        translation = Word.objects.create(content=translation, lang=ru)
        Translation.objects.create(one=word, other=translation)
        logger.info(
            'Translated: "{}" => "{}"',
            word.content, translation.content,
        )
