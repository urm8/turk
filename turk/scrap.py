import pandas as pd
from turk.config import db
from turk.models import Word
from peewee import chunked


if __name__ == '__main__':
    df, = pd.read_html('http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Turkish_WordList_10K')
    db.connect()
    with db.atomic() as transaction:
        for batch in chunked(({'content': row.Word, 'rate': row.Percent.rstrip('%')} for row in df.itertuples()), 100):
            Word.insert_many(batch, ['content', 'rate']).on_conflict_ignore().execute()
    db.close()
