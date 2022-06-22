from django.contrib import admin
from words.models import Example, Language, Translation, Word

admin.site.register(Word)
admin.site.register(Language, search_fields=['code', 'name'])
admin.site.register(
    Translation, search_fields=[
        'one__lang__code', 'one__lang__name' 'one__content', 'other__content',
    ],
)
admin.site.register(Example)
