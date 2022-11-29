from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password1",
            "password2",
            "name",
            "nickname",
            "git_id",
            "boj_id",
        ]


class ProfileForm(forms.ModelForm):
    password = None

    class Meta:
        model = Profile()
        fields = ["image", "nickname", "language", "mbti", "intro"]
        labels = {
            "nickname": "닉네임",
            "language": "사용 언어",
            "mbti": "MBTI",
            "image": "프로필 사진",
            "intro": "소개글",
        }
