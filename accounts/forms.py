from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    password = None
    
    class Meta:
        model = Profile
        fields = ['image', 'nickname', 'github_id', 'boj_id', 'language', 'mbti', 'intro']
        labels = {
            'nickname': '닉네임',
            'language': '사용 언어',
            'mbti': 'MBTI',
            'image': '프로필 사진',
            'intro': '소개글',
            'github_id': 'Github 아이디', 
            'boj_id': '백준 아이디',
        }


class GuestbookArticleForm(forms.ModelForm):
    class Meta:
        model = GuestbookArticle
        fields = ['content']


class GuestbookCommentForm(forms.ModelForm):
    class Meta:
        model = GuestbookComment
        fields = ['content']