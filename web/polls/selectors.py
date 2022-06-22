from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Answer, Poll


def read_random_answer(lang_code: str, answer_type: Answer.Type) -> Answer:
    answer = Answer.objects.filter(
        language_id=lang_code, reason=answer_type,
    ).order_by('?').first()
    if not answer:
        raise Http404('No answer for that type')
    return answer


def read_poll(user_id: int, poll_id: int) -> Poll:
    return get_object_or_404(Poll, poll_id=poll_id, user_id=user_id)
