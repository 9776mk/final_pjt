from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import datetime


# Create your views here.
def signup(request):
    # 이미 로그인 → 회원가입 X
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()

            # 현재 날짜를 기준으로 닉네임 자동 생성
            nickname = str(user.pk) + str(user.date_joined.strftime('%f'))
            Profile.objects.create(user=user, nickname=nickname)
            # 방명록 생성
            return redirect('articles:index')
    else:
        signup_form = CustomUserCreationForm()

    context = {
        'signup_form': signup_form,
    }

    return render(request, 'accounts/signup.html', context)


def login(request):
    # 이미 로그인 → 로그인 X
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        login_form = AuthenticationForm()

    context = {
        'login_form': login_form,
    }

    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


def profile(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)

    context = {
        'user': user,
    }

    return render(request, 'accounts/profile.html', context)


# 회원 정보 수정
@login_required
def profile_update(request, user_pk):
    if request.user.pk != user_pk:
        return redirect('accounts:profile', user_pk)

    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('accounts:profile', user_pk)
    else:
        profile_form = ProfileForm(instance=user.profile)

    context = {
        'user': user,
        'profile_form': profile_form,
    }

    return render(request, "accounts/profile_update.html", context)