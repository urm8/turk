from __future__ import annotations

from django.db.models import Q
from words.models import Translation


def translation_exists(word_id: str, target_lang: str) -> Translation | None:
    """Return translation for word id."""
    return Translation.objects.filter(
        Q(one_id=word_id, other__lang=target_lang) | Q(
            other_id=word_id, one__lang=target_lang,
        ),
    ).first()


def translation_exists_by_word(source, target) -> Translation | None:
    return Translation.objects.filter(
        Q(one=source, other=target) | Q(one=target, other=source),
    ).first()
