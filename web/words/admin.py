from django.contrib import admin
from words.models import Language, Translation, Word

admin.site.register(Word, Language, Translation)
