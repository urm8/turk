import pandas as pd
from django.core.management import BaseCommand
from loguru import logger
from words.models import Word


class Command(BaseCommand):

    def handle(self, *args, **options):
        URL = 'http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Turkish_WordList_10K'  # noqa
        df = pd.read_html(URL)[0]
        for word in df.itertuples():
            logger.info('saving: "{}"', word.Word)
            Word.objects.get_or_create(content=word.Word)
