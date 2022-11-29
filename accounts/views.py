from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import json
from django.http import JsonResponse


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
            Guestbook.objects.create(user=user)
            # 방명록 생성
            return redirect('articles:index')
    else:
        signup_form = CustomUserCreationForm()

    context = {
        'signup_form': signup_form,
    }

    return render(request, 'accounts/signup.html', context)


# 유효한 ID(username)인지 검사
def is_valid_id(request):
    username = json.loads(request.body).get('username')
    # print(username)
    if  len(username) > 0:
        if get_user_model().objects.filter(username=username).exists() :
            is_valid = False
        else:
            is_valid = True

        data = {
            'is_valid': is_valid,
        }

        return JsonResponse(data)
    is_valid = 'null'
    data = {
            'is_valid': is_valid,
        }

    return JsonResponse(data)


def login(request):

    status = 1
    # 이미 로그인 → 로그인 X
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
        else:
            status = 0
            login_form = AuthenticationForm()
            context = {
                'status':status,
                'login_form': login_form,
            }

            return render(request, 'accounts/login.html', context)


    else:
        login_form = AuthenticationForm()

    context = {
        'status':status,
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


# 유저 팔로우/언팔로우
def follow(request, user_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:profile', user.pk)
    
    user = get_object_or_404(get_user_model(), pk=user_pk)
    
    # 나와 다른 유저만 (언)팔로우 가능
    if request.user != user and request.method == 'POST':
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
            is_following = False    # 팔로잉 취소
        else:
            user.followers.add(request.user)
            is_following = True    # 팔로잉

    data = {
        'is_following': is_following,
        'followers_count': user.followers.count(),
    }

    return JsonResponse(data)


# 방명록
def guestbook(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    gb_articles = user.guestbook.guestbookarticle_set.all()
    gb_comments = user.guestbook.guestbookcomment_set.all()

    context = {
        'user': user,
        'gb_articles': gb_articles,
        'gb_comments': gb_comments,
    }

    return render(request, 'accounts/guestbook.html', context)


# 방명록 글 작성
@login_required
def gb_article_create(request, user_pk):
    # if 'gb_article_create' in request.POST:
    if request.method == 'POST':
        gb_article_form = GuestbookArticleForm(request.POST)
        guestbook = get_object_or_404(Guestbook, user_id=user_pk)
        
        if gb_article_form.is_valid():
            gb_article = gb_article_form.save(commit=False)
            gb_article.guestbook = guestbook
            gb_article.user = request.user
            gb_article.save()

        data = {
            'article_pk': gb_article.pk,
            'article_user': gb_article.user.profile.nickname,   # username?
            'article_content': gb_article.content,
            'article_created_at': gb_article.created_at.strftime('%Y.%m.%d'),
        }

        return JsonResponse(data)


# 방명록 글 삭제
@login_required
def gb_article_delete(request, user_pk, gb_article_pk):
    gb_article = get_object_or_404(GuestbookArticle, pk=gb_article_pk)

    is_deleted = False

    if request.user == gb_article.user and request.method == 'POST':
        gb_article.delete()
        # has_comment = True/False
        is_deleted = True

    data = {
        'is_deleted': is_deleted,
    }

    return JsonResponse(data)


# 방명록 댓글 생성
@login_required
def gb_comment_create(request, user_pk, gb_article_pk):
    if request.method == 'POST':
        gb_comment_form = GuestbookCommentForm(request.POST)
        article = get_object_or_404(GuestbookArticle, pk=gb_article_pk)
        guestbook = get_object_or_404(Guestbook, user_id=user_pk)
        
        if gb_comment_form.is_valid():
            comment = gb_comment_form.save(commit=False)
            comment.guestbook = guestbook
            comment.article = article
            comment.user = request.user
            comment.save()

        # data = {
        #     'comment_pk': comment.pk,
        #     'comment_user': comment.user.profile.nickname,   # username?
        #     'comment_content': comment.content,
        #     'comment_created_at': comment.created_at.strftime('%Y.%m.%d'),
        # }

        # return JsonResponse(data)

    return redirect('accounts:guestbook', user_pk)