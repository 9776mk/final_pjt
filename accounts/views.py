from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import json
from django.http import JsonResponse
from django.contrib import messages
# 깃로그인
import os
from dotenv import load_dotenv
import requests
from .exception import *
from .models import *
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import *
from django.utils import timezone  # settings.py의 USE_TZ=True면 datetime 대신 사용


# Create your views here.
def signup(request):
    # 이미 로그인 → 회원가입 X
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        signup_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if signup_form.is_valid() and profile_form.is_valid():
            user = signup_form.save()

            profile = profile_form.save(commit=False)
            Profile.objects.create(
                user=user,
                nickname=profile.nickname,
                github_id=profile.github_id,
                boj_id=profile.boj_id,
            )
            Guestbook.objects.create(user=user)  # 방명록 생성
            # 회원가입 후 자동로그인
            auth_login(
                request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("home")
    else:
        signup_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    context = {
        "signup_form": signup_form,
        "profile_form": profile_form,
    }

    return render(request, "accounts/signup.html", context)


# 유효한 ID(username)인지 검사
def is_valid_id(request):
    username = json.loads(request.body).get("username")
    # print(username)
    if len(username) > 0:
        if get_user_model().objects.filter(username=username).exists():
            is_valid = False
        else:
            is_valid = True

        data = {
            "is_valid": is_valid,
        }

        return JsonResponse(data)
    is_valid = "null"
    data = {
        "is_valid": is_valid,
    }

    return JsonResponse(data)


def login(request):
    status = 1
    # 이미 로그인 → 로그인 X
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            response = redirect(request.GET.get("next") or "home")
            notes_counter = Notes.objects.filter(to_user_id=request.user.id, read=0, garbage=False).count()
            request.user.message_number = notes_counter
            request.user.save()
            return response
        else:
            status = 0
            login_form = AuthenticationForm()
            context = {
                "status": status,
                "login_form": login_form,
            }

            return render(request, "accounts/login.html", context)
    else:
        login_form = AuthenticationForm()

    context = {
        "status": status,
        "login_form": login_form,
    }

    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("home")


def profile(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    followers = user.followers.all()
    followings = user.followings.all()

    # 백준에서 id로 정보 받아오기
    url = "https://solved.ac/api/v3/user/show"
    profile_info = Profile.objects.get(pk=user_pk)
    id = profile_info.boj_id
    if id:
        querystring = {"handle": {id}}
        headers = {"Content-Type": "application/json"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            tier = response.json()["tier"]
        else:
            tier = -1
    else:
        tier = 0
    
    profile_info.boj_tier = tier
    profile_info.save()

    context = {
        "user": user,
        "followers": followers,
        "followings": followings,
        "tier": tier,
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

# git 로그인 클릭시 git으로 정보를 보냄
def github_login(request):
    client_id = GITHUB_CLIENT_ID
    redirect_uri = "http://127.0.0.1:8000/accounts/login/github/callback/"
    scope = "read:user"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )


# git에서 로그인 유저 정보
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

    # DB에 깃허브 정보 저장
    user_info = login_data[service_name]

    print(user_info["social_id"])  # 62585191
    print(user_info["username"])  # jupiter6676
    print(user_info["social_profile_picture"])

    # 이미 연동된 유저는 로그인
    if get_user_model().objects.filter(social_id=user_info["social_id"]).exists():
        user = get_user_model().objects.get(social_id=user_info["social_id"])
        auth_login(request, user)
        return redirect(request.GET.get("next") or "/")
    # 연동이 처음이면 회원가입 (DB에 저장)
    else:
        # data = {
        #     # 일반 정보
        #     "name": (profile_json["name"]),
        #     "username": (profile_json["login"]),
        #     "git_id": (profile_json["login"]),
        # }

        # signup_form = CustomUserCreationForm(initial=data)
        # context = {
        #     "signup_form": signup_form,
        # }

        now = timezone.now()
        username = str(user_info["social_id"]) + str(now.strftime("%f"))
        user = get_user_model().objects.create(
            username=username, date_joined=now, social_id=user_info["social_id"]
        )
        Profile.objects.create(
            user=user,
            nickname=user_info["social_id"],
            github_id=user_info["username"],
            image=user_info["social_profile_picture"],
        )
        Guestbook.objects.create(user=user)

        return redirect("/")


# 유저 팔로우/언팔로우
def follow(request,user_pk):
    if not request.user.is_authenticated:
        return redirect("accounts:profile", user.pk)

    user = get_object_or_404(get_user_model(), pk=user_pk)

    # 나와 다른 유저만 (언)팔로우 가능
    if request.user != user and request.method == "POST":
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
            is_following = False  # 팔로잉 취소
            messages.warning(request,"님 팔로워 취소함")
        else:
            user.followers.add(request.user)
            is_following = True  # 팔로잉
            messages.warning(request,"님 팔로워함")

    if not request.user.profile.image:
        my_image = "/static/images/no-avatar.jpg"
    elif str(request.user.profile.image)[:4] == "http":
        my_image = str(request.user.profile.image)
    else:
        my_image = str(request.user.profile.image.url)

    if not user.profile.image:
        user_image = "/static/images/no-avatar.jpg"
    elif str(user.profile.image)[:4] == "http":
        user_image = str(user.profile.image)
    else:
        user_image = str(user.profile.image.url)

    data = {
        # 다른 유저 페이지에서 그 유저를 (언)팔로우
        "is_following": is_following,
        "followers_count": user.followers.count(),
        "followings_count": user.followings.count(),
        "my_image": my_image,
        "my_username": request.user.username,
        "my_nickname": request.user.profile.nickname,

        # 나의 페이지에서 다른 유저를 (언)팔로우
        "my_user_pk": request.user.pk,
        "my_followers_count": request.user.followers.count(),
        "my_followings_count": request.user.followings.count(),
        "user_image": user_image,
        "user_username": user.username,
        "user_nickname": user.profile.nickname,
    }

    return JsonResponse(data)


# 방명록
def guestbook(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    gb_articles = user.guestbook.guestbookarticle_set.all().order_by("-pk")
    gb_comments = user.guestbook.guestbookcomment_set.all()

    context = {
        "user": user,
        "gb_articles": gb_articles,
        "gb_comments": gb_comments,
    }

    return render(request, "accounts/guestbook.html", context)


# 방명록 글 작성
@login_required
def gb_article_create(request, user_pk):
    # if 'gb_article_create' in request.POST:
    if request.method == "POST":
        gb_article_form = GuestbookArticleForm(request.POST)
        guestbook = get_object_or_404(Guestbook, user_id=user_pk)
        is_secret = True if request.POST.get("is_secret") == "true" else False

        if gb_article_form.is_valid():
            gb_article = gb_article_form.save(commit=False)
            gb_article.guestbook = guestbook
            gb_article.user = request.user
            gb_article.is_secret = is_secret
            gb_article.save()

        # 프사 X: images/unknown1111_MLNFs1A.jpg
        # 깃허브 프사: https://avatars.githubusercontent.com/u/62585191?v=4
        # 파일로 올린 프사: /static/images/no-avatar.jpg
        if not gb_article.user.profile.image:
            article_user_image = "/static/images/no-avatar.jpg"
        elif str(gb_article.user.profile.image)[:4] == "http":
            article_user_image = str(gb_article.user.profile.image)
        else:
            article_user_image = str(gb_article.user.profile.image.url)

        data = {
            "article_pk": gb_article.pk,
            "article_user": gb_article.user.profile.nickname,  # username?
            "article_content": gb_article.content,
            "article_created_at": gb_article.created_at.strftime("%Y.%m.%d"),
            "article_user_image": article_user_image,
            "article_is_secret": is_secret,
        }

        return JsonResponse(data)


# 방명록 글 삭제
@login_required
def gb_article_delete(request, user_pk, gb_article_pk):
    gb_article = get_object_or_404(GuestbookArticle, pk=gb_article_pk)

    is_deleted = False

    if request.user == gb_article.user and request.method == "POST":
        gb_article.delete()
        # has_comment = True/False
        is_deleted = True

    data = {
        "is_deleted": is_deleted,
    }

    return JsonResponse(data)


# 방명록 댓글 생성
@login_required
def gb_comment_create(request, user_pk, gb_article_pk):
    if request.method == "POST":
        gb_comment_form = GuestbookCommentForm(request.POST)
        article = get_object_or_404(GuestbookArticle, pk=gb_article_pk)
        guestbook = get_object_or_404(Guestbook, user_id=user_pk)

        if request.POST.get("is_secret") == "true" or article.is_secret == True:
            is_secret = True
        else:
            is_secret = False

        if gb_comment_form.is_valid():
            comment = gb_comment_form.save(commit=False)
            comment.guestbook = guestbook
            comment.article = article
            comment.user = request.user
            comment.is_secret = is_secret
            comment.save()

        if not comment.user.profile.image:
            comment_user_image = "/static/images/no-avatar.jpg"
        elif str(comment.user.profile.image)[:4] == "http":
            comment_user_image = str(comment.user.profile.image)
        else:
            comment_user_image = str(comment.user.profile.image.url)

        data = {
            "comment_pk": comment.pk,
            "comment_user": comment.user.profile.nickname,  # username?
            "comment_content": comment.content,
            "comment_created_at": comment.created_at.strftime("%Y.%m.%d"),
            "comment_user_image": comment_user_image,
            "article_is_secret": article.is_secret,
            "comment_is_secret": is_secret,
        }

        return JsonResponse(data)

    return redirect("accounts:guestbook", user_pk)


# 방명록 댓글 삭제
@login_required
def gb_comment_delete(request, user_pk, gb_article_pk, gb_comment_pk):
    gb_comment = get_object_or_404(GuestbookComment, pk=gb_comment_pk)
    gb_article = get_object_or_404(GuestbookArticle, pk=gb_article_pk)

    if request.user == gb_comment.user and request.method == "POST":
        gb_comment.delete()

    # 방명록 글에 작성된 답글의 개수
    total_comment_cnt = gb_article.guestbookcomment_set.count()

    data = {
        "total_comment_cnt": total_comment_cnt,
    }

    return JsonResponse(data)


