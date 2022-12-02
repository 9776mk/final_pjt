from django.db import models


class BJData(models.Model):
    level = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
