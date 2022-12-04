from django.db import models

# 백준 브론즈
class BJData_br(models.Model):
    level = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=50)
    tags = models.CharField(max_length=50)


# 백준 실버
class BJData_si(models.Model):
    level = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=50)
    tags = models.CharField(max_length=50)


# 백준 골드
class BJData_go(models.Model):
    level = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=50)
    tags = models.CharField(max_length=50)


# 백준 플레
class BJData_pl(models.Model):
    level = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=50)
    tags = models.CharField(max_length=50)


# 백준 다이아
class BJData_di(models.Model):
    level = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=50)
    tags = models.CharField(max_length=50)


# 백준 루비
class BJData_ru(models.Model):
    level = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=50)
    tags = models.CharField(max_length=50)
