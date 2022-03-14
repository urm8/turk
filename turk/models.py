import peewee
from .config import db


class Word(peewee.Model):
    content = peewee.CharField(unique=True, null=False)
    rate = peewee.DecimalField(max_digits=16, decimal_places=14, null=True, index=True)

    class Meta:
        database = db
Word.add_index(peewee.SQL('create index if not exists word_rate_desc on word (rate desc);'))

class Translation(peewee.Model):
    word = peewee.ForeignKeyField(Word, backref='translations')
    content = peewee.CharField(unique=True, null=False)

    class Meta:
        database = db