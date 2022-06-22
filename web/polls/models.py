from django.db import models


class Poll(models.Model):
    user_id = models.CharField(max_length=256, db_index=True)
    poll_id = models.CharField(max_length=256, db_index=True, primary_key=True)
    is_closed = models.BooleanField(default=False)
    correct_option_id = models.IntegerField()
    closed = models.BooleanField(default=False)
    chat_id = models.IntegerField()


class UserLanguage(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    native_language = models.ForeignKey(
        to='words.Language', on_delete=models.CASCADE, blank=False, null=False, related_name='+',
    )
    learn_language = models.ForeignKey(
        to='words.Language', on_delete=models.CASCADE, blank=False, null=False, related_name='+',
    )

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'user_id={self.user_id}, {self.native_language_id} => {self.learn_language_id}'


class UserWord(models.Model):
    user_id = models.BigIntegerField()
    word = models.ForeignKey(
        to='words.Word', on_delete=models.CASCADE, blank=False, null=False,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                'user_id', 'word', name='uniq__user_word',
            ),
        )


class PollStats(models.Model):
    """Track stats for each user."""
    user_id = models.BigIntegerField(primary_key=True)
    total_attempts = models.IntegerField(default=0, blank=True)
    correct_answers = models.IntegerField(default=0, blank=True)


class Answer(models.Model):
    """Store pre-existing answers for different cases."""

    class Type(models.TextChoices):
        correct = 'correct'
        incorrect = 'incorrect'
        cheer_up = 'cheer_up'

    reason = models.CharField(max_length=32, choices=Type.choices)
    language = models.ForeignKey(
        'words.Language', on_delete=models.CASCADE, blank=False, default='en',
    )
    content = models.TextField(blank=False)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'Answer("{self.language}", "{self.content}", "{self.Type(self.reason).label}")'
