from django.contrib import admin
from polls.models import Answer, Poll, PollStats, UserLanguage, UserWord

admin.site.register(Poll)
admin.site.register(PollStats)
admin.site.register(
    Answer, list_filter=[
        'reason',
    ], autocomplete_fields=['language'],
)
admin.site.register(UserLanguage)
admin.site.register(UserWord)
