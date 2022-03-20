"""Basic script that imports most popular words from wiki page."""
import asyncio
from loguru import logger

import pandas as pd

from turk.config import init_db
from turk.models import Word

URL = 'http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Turkish_WordList_10K'  # noqa


async def run():
    """Load table from wiki page."""
    await init_db()
    df = pd.read_html(URL)[0]
    for word in df.itertuples():
        logger.info('saving: "{}"', word.Word)
        await Word.get_or_create(
            {'rate': word.Percent.rstrip('%')}, word=word.Word
        )


if __name__ == '__main__':
    asyncio.run(run())
