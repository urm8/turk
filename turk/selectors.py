"""Simple selectors used in services."""
from tortoise.functions import Function
from tortoise.queryset import QuerySet

from turk.models import Word


def read_random(count: int, *, from_top: int = 100) -> QuerySet[Word]:
    """Return random word.

    Args:
        count (int): amount of words to return
        from_top (int): selects words only from most popular list.

    Returns:
        Iterable[Word]: built query
    """
    top_qs = Word.all().order_by('-rate').limit(from_top).values('id')
    return (
        Word.
        filter(id__in=top_qs).
        annotate(rnd=Function('RANDOM')).
        order_by('rnd')
    )


def read_without_translation() -> QuerySet[Word]:
    """Read unstranslated words.

    Returns:
        words that don't have translation.
    """
    return (
        Word.
        all().
        prefetch_related('translations').
        filter(translations__isnull=True)
    )
