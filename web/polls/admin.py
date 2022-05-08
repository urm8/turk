from django.contrib import admin
from polls.models import Answer, Poll, PollStats

admin.site.register(Poll, PollStats, Answer)
