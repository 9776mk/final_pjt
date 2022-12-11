from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from imagekit.processors import ResizeToFill
from multiselectfield import MultiSelectField
from notes.models import Notes
from studies.models import StudyNotice

# Create your models here.
class User(AbstractUser):
    # username = models.CharField(max_length=16, unique=True)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    username = models.CharField(
        error_messages={"unique": "같은 아이디가 이미 존재합니다."},
        unique=True,
        max_length=16,
        validators=[UnicodeUsernameValidator()],
        verbose_name="아이디",
    )
    # 선택 항목 필드
    # name = models.CharField(max_length=20, null=True, blank=True)
    # nickname = models.CharField(max_length=20, null=True, blank=True)
    # profile_picture = ProcessedImageField(
    #     upload_to="profile_pictures/",
    #     null=True,
    #     blank=True,
    #     processors=[ResizeToFill(512, 512)],
    #     format="JPEG",
    #     options={
    #         "quality": 80,
    #     },
    # )
    # 소셜 아이디 관련 필드
    is_social_account = models.BooleanField(default=False)
    git_id = models.CharField(null=True, blank=True, max_length=50)
    boj_id = models.CharField(null=True, blank=True, max_length=50)
    service_name = models.CharField(null=True, max_length=20)
    social_id = models.CharField(null=True, blank=True, max_length=100)
    social_profile_picture = models.CharField(null=True, blank=True, max_length=150)
    # 인증 필드
    token = models.CharField(max_length=150, null=True, blank=True)
    notice_note = models.BooleanField(default=True)  # 쪽지
    note_notice = models.BooleanField(default=True)  # 쪽지

    # 쪽지 알림 개수
    @property
    def get_message_notice_cnt(self):
        message_notice_cnt = Notes.objects.filter(to_user=self, read=0, garbage=False).count()
        return message_notice_cnt

    # 스터디 알림 개수
    @property
    def get_study_notice_cnt(self):
        study_notice_cnt = StudyNotice.objects.filter(user=self, read=False).count()
        return study_notice_cnt

    # 스터디 알림 리스트
    @property
    def get_study_notice(self):
        study_notice_list = StudyNotice.objects.filter(user=self)

        # 읽음 처리
        # for notice in study_notice_list:
        #     notice.read = True
        #     notice.save()

        return study_notice_list



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=16)
    intro = models.TextField(blank=True)
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[Thumbnail(200, 200)],
        format="JPEG",
        options={"quality": 50},
    )

    # 프로그래밍 언어 선택
    # 앞: DB에 저장되는 값, 뒤: admin이나 form에서 표시하는 값
    LANGUAGE_CHOICE = (
        ("JavaScript", "JavaScript"),
        ("Java", "Java"),
        ("Python", "Python"),
        ("C", "C"),
        ("C++", "C++"),
        ("PHP", "PHP"),
    )
    language = models.CharField(blank=True, max_length=10, choices=LANGUAGE_CHOICE)
    STACK = (
        ("Django", "Django"),
        ("Spring", "Spring"),
        ("Node.js", "Node.js"),
        ("React", "React"),
        ("MySQL", "MySQL"),
        ("SQLite", "SQLite"),
    )
    stack = MultiSelectField(blank=True, choices=STACK)

    # MBTI 유형 선택
    MBTI_CHOICE = (
        ("ISTJ", "ISTJ"),
        ("ISTP", "ISTP"),
        ("ISFJ", "ISFJ"),
        ("ISFP", "ISFP"),
        ("INTJ", "INTJ"),
        ("INTP", "INTP"),
        ("INFJ", "INFJ"),
        ("INFP", "INFP"),
        ("ESTJ", "ESTJ"),
        ("ESTP", "ESTP"),
        ("ESFJ", "ESFJ"),
        ("ESFP", "ESFP"),
        ("ENTJ", "ENTJ"),
        ("ENTP", "ENTP"),
        ("ENFJ", "ENFJ"),
        ("ENFP", "ENFP"),
    )
    mbti = models.CharField(blank=True, max_length=4, choices=MBTI_CHOICE)

    # 깃허브, 백준 ID
    github_id = models.CharField(blank=True, max_length=20)
    boj_id = models.CharField(blank=True, max_length=20)
    # 백준 티어
    boj_tier = models.IntegerField(blank=True, default=0)


# 방명록 (User와 1:1)
class Guestbook(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# 방명록 글
class GuestbookArticle(models.Model):
    guestbook = models.ForeignKey(
        Guestbook, on_delete=models.CASCADE
    )  # 어느 방명록에 글이 쓰였는지
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # 글을 누가 썼는지
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_secret = models.BooleanField(default=False)


# 방명록 댓글
class GuestbookComment(models.Model):
    guestbook = models.ForeignKey(
        Guestbook, on_delete=models.CASCADE
    )  # 어느 방명록에 글이 쓰였는지
    article = models.ForeignKey(GuestbookArticle, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_secret = models.BooleanField(default=False)


# https://github.com/login/oauth/authorize?client_id=None&redirect_uri=http://127.0.0.1:8000/accounts/login/github/callback/&scope=read:user
