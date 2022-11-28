from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


# Create your models here.
class User(AbstractUser):
    # username = models.CharField(max_length=16, unique=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    username = models.CharField(max_length=16, unique=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=16)
    intro = models.TextField(blank=True)
    image = ProcessedImageField(
        upload_to='images/',
        blank=True,
        processors=[Thumbnail(200, 200)],
        format='JPEG',
        options={'quality': 50},
    )

    # 프로그래밍 언어 선택
    # 앞: DB에 저장되는 값, 뒤: admin이나 form에서 표시하는 값
    LANGUAGE_CHOICE = (
        ('C', 'C'),
        ('Python', 'Python'),
        ('Java', 'Java'),
    )
    language = models.CharField(blank=True, max_length=10, choices=LANGUAGE_CHOICE)

    # MBTI 유형 선택
    MBTI_CHOICE = (
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('INFJ', 'INFJ'), ('INTJ', 'INTJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('INFP', 'INFP'), ('INTP', 'INTP'),
        ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'), ('ENFJ', 'ENFJ'), ('ENTJ', 'ENTJ'),
        ('ESTP', 'ESTP'), ('ESFP', 'ESFP'), ('ENFP', 'ENFP'), ('ENTP', 'ENTP'),
    )
    mbti = models.CharField(blank=True, max_length=4, choices=MBTI_CHOICE)

    # 깃허브, 백준 ID
    github_id = models.CharField(blank=True, max_length=20)
    boj_id = models.CharField(blank=True, max_length=20)