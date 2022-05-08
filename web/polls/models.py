from django.db import models


class Poll(models.Model):
    pass


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
        'words.Language', on_delete=models.CASCADE, blank=False,
    )
    content = models.TextField(blank=False)
