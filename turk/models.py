import peewee
from .config import db


class Word(peewee.Model):
    content = peewee.CharField(unique=True, null=False)
    rate = peewee.DecimalField(max_digits=16, decimal_places=14, null=True, index=True)

    class Meta:
        database = db

    def __str__(self):
        return repr(self)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.content}, {self.rate})'

Word.add_index(peewee.SQL('create index if not exists word_rate_desc on word (rate desc);'))

class Translation(peewee.Model):
    word = peewee.ForeignKeyField(Word, backref='translations')
    content = peewee.CharField(unique=True, null=False)

    class Meta:
        database = db
        indexes = (
             (('word_id', 'content'), True),
        )
    
    