from turk.models import Translation, Word
from peewee import fn

from typing import Iterable


def read_random(count: int, *, from_top: int = 100) -> Iterable[Word]:
    cte = Word.select().order_by(-Word.rate).limit(from_top)
    return Word.select().join(cte, on=(Word.id == cte.c.id)).order_by(fn.Random()).limit(count)


def read_without_translation():
    return Word.select().left_outer_join(Translation).where(Translation.id.is_null())