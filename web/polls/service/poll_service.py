from polls.models import Poll


def add_poll(user_id: int, chat_id: int, poll_id: int, correct_option_id: int) -> Poll:
    return Poll.objects.create(
        user_id=user_id,
        chat_id=chat_id,
        poll_id=poll_id,
        correct_option_id=correct_option_id,
    )
