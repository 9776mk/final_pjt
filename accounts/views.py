from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import json
from django.http import JsonResponse

# 깃로그인
import os
from dotenv import load_dotenv
import requests
from .exception import *
from .models import *
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import *


# Create your views here.
def signup(request):
    # 이미 로그인 → 회원가입 X
    if request.user.is_authenticated:
        return redirect("articles:index")

    if request.method == "POST":
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()

            # 현재 날짜를 기준으로 닉네임 자동 생성
            nickname = str(user.pk) + str(user.date_joined.strftime("%f"))
            Profile.objects.create(user=user, nickname=nickname)
            # 방명록 생성
            return redirect("articles:index")
    else:
        signup_form = CustomUserCreationForm()

    context = {
        "signup_form": signup_form,
    }

    return render(request, "accounts/signup.html", context)


# 유효한 ID(username)인지 검사
def is_valid_id(request):
    username = json.loads(request.body).get("username")
    # print(username)

    if get_user_model().objects.filter(username=username).exists():
        print("false")
        is_valid = False
    else:
        is_valid = True

    data = {
        "is_valid": is_valid,
    }

    return JsonResponse(data)


def login(request):
    # 이미 로그인 → 로그인 X
    if request.user.is_authenticated:
        return redirect("articles:index")

    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get("next") or "articles:index")
    else:
        login_form = AuthenticationForm()

    context = {
        "login_form": login_form,
    }

    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("articles:index")


def profile(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)

    context = {
        "user": user,
    }

    return render(request, "accounts/profile.html", context)


# 회원 정보 수정
@login_required
def profile_update(request, user_pk):
    if request.user.pk != user_pk:
        return redirect("accounts:profile", user_pk)

    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect("accounts:profile", user_pk)
    else:
        profile_form = ProfileForm(instance=user.profile)

    context = {
        "user": user,
        "profile_form": profile_form,
    }

    return render(request, "accounts/profile_update.html", context)


# 깃 로그인용
load_dotenv()
GITHUB_CLIENT_ID = os.getenv("GIT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GIT_CLIENT_SECRET")


def github_login(request):
    client_id = GITHUB_CLIENT_ID
    redirect_uri = "http://127.0.0.1:8000/accounts/login/github/callback/"
    scope = "read:user"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )


def github_login_callback(request):
    if request.user.is_authenticated:
        raise SocialLoginException("User already logged in")
    code = request.GET.get("code", None)
    if code is None:
        raise GithubException("Can't get code")

    client_id = GITHUB_CLIENT_ID
    client_secret = GITHUB_CLIENT_SECRET

    token_request = requests.post(
        f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
        headers={"Accept": "application/json"},
    )
    token_json = token_request.json()
    print(token_json)
    error = token_json.get("error", None)

    if error is not None:
        raise GithubException("Can't get access token")

    access_token = token_json.get("access_token")

    profile_request = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"token {access_token}",
            "Accept": "application/json",
        },
    )
    print(profile_request)

    profile_json = profile_request.json()

    # username = profile_json.get("login", None)
    # avatar_url = profile_json.get("avatar_url", None)
    # name = profile_json.get("name", None)
    # email = profile_json.get("email", None)
    # print(f"{username}, {avatar_url}, {name}, {email}")
    # 여기까지 확인

    service_name = "github"
    profile_json = profile_request.json()
    print(profile_json)
    login_data = {
        "github": {
            "social_id": profile_json["id"],
            "username": profile_json["login"],
            "social_profile_picture": profile_json["avatar_url"],
            "nickname": profile_json["bio"],
            "email": profile_json["email"],
            ### 깃허브에서만 가져오는 항목 ###
            "git_id": profile_json["login"],
            ### 깃허브에서만 가져오는 항목 ###
        },
    }
    user_info = login_data[service_name]
    if get_user_model().objects.filter(social_id=user_info["social_id"]).exists():
        user = get_user_model().objects.get(social_id=user_info["social_id"])
        auth_login(request, user)
        return redirect(request.GET.get("next") or "reviews:index")
    else:
        data = {
            # 일반 정보
            "name": (profile_json["name"]),
            "username": (profile_json["login"]),
            "git_id": (profile_json["login"]),
        }
        signup_form = CustomUserCreationForm(initial=data)
        context = {
            "signup_form": signup_form,
        }
        return render(request, "accounts/signup.html", context)
