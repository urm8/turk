from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'Language("{self.code}")'


class Word(models.Model):
    content = models.CharField(max_length=512)
    lang = models.ForeignKey(
        'words.Language', on_delete=models.CASCADE, related_name='+',
    )

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'Word("{self.content}", "{self.lang_id}")'


class Translation(models.Model):
    one = models.ForeignKey(
        Word, on_delete=models.CASCADE, null=False, related_name='+',
    )
    other = models.ForeignKey(
        Word, on_delete=models.CASCADE, null=False, related_name='+',
    )

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f'T("{self.one} <-> {self.other}")'


class Example(models.Model):
    word = models.ForeignKey(to=Word, on_delete=models.CASCADE)
    lang = models.ForeignKey(to=Language, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
