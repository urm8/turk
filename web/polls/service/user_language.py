from django.db import transaction
from loguru import logger
from polls.models import UserLanguage, UserWord


def set_user_language(user_id: int, native_language: str, learn_language) -> UserLanguage:
    with transaction.atomic():
        ulang, created = UserLanguage.objects.update_or_create(
            user_id=user_id,
            defaults={
                'user_id': user_id,
                'native_language_id': native_language,
                'learn_language_id': learn_language,
            },
        )
        logger.info(
            '{} {} language to {}',
            'set' if created else 'updated', user_id, learn_language,
        )
        UserWord.objects.filter(user_id=user_id).delete()
        return ulang
