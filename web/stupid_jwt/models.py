from django.db import models

# Create your models here.


class JWTToken(models.Model):
    body = models.CharField(max_length=512, blank=False)
