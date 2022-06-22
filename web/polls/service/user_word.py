from django.db.models import Exists, OuterRef
from polls.models import UserLanguage, UserWord
from words.models import Translation, Word


def add_word(user_id: int, word_id: int) -> UserWord:
    return UserWord.objects.create(user_id=user_id, word_id=word_id)


def read_random_words(user_id: int) -> Word:
    ul = UserLanguage.objects.get(user_id=user_id)
    return Word.objects.filter(
        Exists(
            UserWord.objects.filter(
                user_id=user_id, word_id=OuterRef('id'),
            ),
        ),
        Exists(
            Translation.objects.filter(
                one=OuterRef(
                    'pk',
                ), other__lang=ul.learn_language_id,
            ),
        ),
        lang_id=ul.native_language_id,
    ).order_by('?')
