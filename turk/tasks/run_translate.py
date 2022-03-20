import logging
import time
from random import random
from googletrans import Translator

from turk.config import db
from turk.models import Translation
from turk.selectors import read_without_translation

logger = logging.getLogger(__name__)

def run():
    translator = Translator()
    with db:
        for word in read_without_translation().paginate(1, 100):
            translation = translator.translate(word.content, 'ru', 'tr')
            logger.info(f'Translated: {word.content} => {translation}')
            Translation.create(word=word, content=translation)
            time.sleep(random() * 4)
        


if __name__ == '__main__':
    run()