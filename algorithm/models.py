from django.db import models


class BJData_1(models.Model):
    level = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=50)
    tags = models.CharField(max_length=20)
