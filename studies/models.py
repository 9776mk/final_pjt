from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.
class Study(models.Model):
    # 1. 스터디장
    host_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 2. 스터디 종류
    CATEGORY = (
        ('알고리즘 공부', '알고리즘 공부'),
        ("프론트엔드 공부", "프론트엔드 공부"),
        ("백엔드 공부", "백엔드 공부"),
        ("기타", "기타"),
    )
    category = models.CharField(max_length=10, choices=CATEGORY)

    # 3. 스터디명
    title = models.CharField(max_length=10)

    # 4. 스터디 소개
    content = models.TextField()

    # 5. 최대 인원
    limit = models.IntegerField(default=2)

    # 6. 모집 마감 여부
    is_closed = models.BooleanField(default=False)

    # 7. 연락처
    contact = models.CharField(max_length=50)

    # 8. 이미지
    image = ProcessedImageField(
        upload_to = 'study_images/',
        processors=[Thumbnail(300, 300)],
        format='JPEG',
        options={'quality': 60}
    )


class List(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)    # False: 가입 대기, True: 가입 승인


class StudyNotice(models.Model):
    study_title = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    noticed_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)