"""Contains mappers for common tables."""
from tortoise import fields
from tortoise.models import Model
from tortoise.indexes import Index

MAX_DIGITS = 16
MAX_WORD_LEN = 128
DECIMAL_PLACES = 10


class Word(Model):
    """Basic mapper for word table.

    Acts as a source for translation.
    """

    id = fields.IntField(pk=True)
    word = fields.CharField(max_length=MAX_WORD_LEN, unique=True, null=False)
    rate = fields.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        null=True,
        index=True,
    )

    def __str__(self):  # noqa: D105
        return repr(self)

    def __repr__(self) -> str:  # noqa: D105
        return 'Word({0}, {1})'.format(self.word, self.rate)


class Translation(Model):
    """Basic mapper for translation to target language."""

    id = fields.BigIntField(pk=True)
    word = fields.ForeignKeyField('models.Word', related_name='translations')
    translation = fields.CharField(
        max_length=MAX_WORD_LEN, null=False,
    )

    class Meta:
        indexes = (
            Index(fields={'word_id', 'translation'}),
        )
