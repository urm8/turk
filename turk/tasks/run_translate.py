"""Translates words from db."""
import asyncio
from loguru import logger

from translate import Translator

from turk.config import init_db
from turk.models import Translation
from turk.selectors import read_without_translation



async def run():
    """Stupid function that translates words."""
    await init_db()
    logger.info('start')
    translator = Translator(to_lang='ru', from_lang='tr')
    async for word in read_without_translation():
        logger.debug('handle: {}')
        translation = translator.translate(word.word)
        logger.info('Translated: "{}" => "{}"', word.word, translation)
        value = dict(word=word, translation=translation)
        if not await Translation.filter(**value).exists():
            await Translation.create(**value)



if __name__ == '__main__':
    asyncio.run(run())
