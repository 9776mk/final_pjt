from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, ArticleComment, Image
from .forms import articleForm, ArticleCommentForm, ImageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import Profile
from django.core.paginator import Paginator
from algorithm.models import (
    BJData_br,
    BJData_si,
    BJData_go,
    BJData_pl,
    BJData_di,
    BJData_ru,
)
from datetime import date, datetime, timedelta
import random

# Create your views here.


def home(request):
    # 파이썬이 주 언어인 사람 가져옴
    python = Profile.objects.filter(language="Python")
    C = Profile.objects.filter(language="C")
    Java = Profile.objects.filter(language="Java")
    Cp = Profile.objects.filter(language="C++")
    JavaScript = Profile.objects.filter(language="JavaScript")
    PHP = Profile.objects.filter(language="PHP")

    Cp_cnt = len(Cp)
    JavaScript_cnt = len(JavaScript)
    PHP_cnt = len(PHP)
    python_cnt = len(python)
    C_cnt = len(C)
    Java_cnt = len(Java)

    Cp_re = 0
    JavaScript_re = 0
    PHP_re = 0

    python_re = 0
    C_re = 0
    Java_re = 0
    re_li = [Cp_re, JavaScript_re, PHP_re, python_re, C_re, Java_re]
    cnt_li = [Cp_cnt, JavaScript_cnt, PHP_cnt, python_cnt, C_cnt, Java_cnt]
    # 비율 계산
    for i in range(len(re_li)):
        if cnt_li[i] != 0:
            re_li[i] = round(
                (
                    cnt_li[i]
                    / (
                        python_cnt
                        + Java_cnt
                        + C_cnt
                        + Cp_cnt
                        + JavaScript_cnt
                        + PHP_cnt
                    )
                )
                * 100
            )
    dic = {
        "C++": re_li[0],
        "JavaScript": re_li[1],
        "PHP": re_li[2],
        "Python": re_li[3],
        "C": re_li[4],
        "Java": re_li[5],
    }
    sorted_dict = sorted(dic.items(), key=lambda item: item[1], reverse=True)

    티어 = ["br", "si", "go", "pl", "di", "ru"]
    DB_li = [BJData_br, BJData_si, BJData_go, BJData_pl, BJData_di, BJData_ru]
    # 비동기 처리,,,
    if "targetTi" in request.GET.keys():
        cur = 0
        nums = []
        titles = []
        ti = request.GET["targetTi"]
        for i in range(6):
            if ti == 티어[i]:
                c = i
                result = DB_li[i].objects.all()
                for re in result:
                    nums.append(re.number)
        nums = random.choice(nums)
        titles = DB_li[c].objects.get(number=nums).title
        tags = DB_li[c].objects.get(number=nums).tags
        data = {"num": nums, "title": titles, "tags": tags}
        return JsonResponse(data)

    context = {
        "sorted_dict": sorted_dict,
    }
    return render(request, "articles/home.html", context)


def index(request):
    # page = request.GET.get('page', '1')은
    # http://localhost:8000/pybo/?page=1 처럼
    # GET 방식으로 호출된 URL에서 page값을 가져올 때 사용한다.
    # 만약 http://localhost:8000/pybo/ 처럼 page값 없이 호출된 경우에는
    # 디폴트로 1이라는 값을 설정한다.
    page = request.GET.get("page", "1")  # 페이지
    articles = Article.objects.order_by("-pk")
    paginator = Paginator(articles, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)  # 마지막 페이지 번호

    context = {
        "articles": page_obj,
        "max_index": max_index,
    }
    return render(request, "articles/index.html", context)


def friend(request):
    return render(request, "articles/friend.html")


@login_required
def create(request):
    if request.method == "POST":
        article_form = articleForm(request.POST)
        # 이미지 폼
        image_form = ImageForm(request.POST, request.FILES)
        tmp_images = request.FILES.getlist("image")

        if article_form.is_valid() and image_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()

            if tmp_images:
                for img in tmp_images:
                    img_instance = Image(article=article, image=img)
                    img_instance.save()

            return redirect("articles:index")

    else:
        article_form = articleForm()
        image_form = ImageForm()

    context = {
        "article_form": article_form,
        "image_form": image_form,
    }
    return render(request, "articles/create.html", context)


def detail(request, pk):
    articles = Article.objects.get(pk=pk)
    comment_form = ArticleCommentForm()
    context = {
        "articles": articles,
        "image_cnt": articles.image_set.count(),
        "comments": articles.articlecomment_set.all(),
        "comment_form": comment_form,
    }
    response = render(request, "articles/detail.html", context)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(seconds=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()
    cookie_value = request.COOKIES.get("hitboard", "_")

    if f"_{pk}_" not in cookie_value:
        cookie_value += f"{pk}_"
        response.set_cookie(
            "hitboard", value=cookie_value, max_age=max_age, httponly=True
        )
        articles.hits += 1
        articles.save()
    return response


@login_required
def update(request, pk):
    articles = get_object_or_404(Article, pk=pk)
    images = Image.objects.filter(article_id=pk)  # 기존 이미지

    if request.user == articles.user:
        if request.method == "POST":
            article_form = articleForm(request.POST, request.FILES, instance=articles)
            image_form = ImageForm(request.POST, request.FILES)
            tmp_images = request.FILES.getlist("image")

            # 기존 이미지 삭제
            for img in images:
                if img:
                    img.delete()

            if article_form.is_valid() and image_form.is_valid():
                article = article_form.save(commit=False)
                article.user = request.user
                article.save()

                if tmp_images:
                    for img in tmp_images:
                        img_instance = Image(article=article, image=img)
                        img_instance.save()

            return redirect("articles:detail", pk)
        else:
            article_form = articleForm(instance=articles)
            image_form = ImageForm()
        context = {
            "article_form": article_form,
            "image_form": image_form,
            "articles": articles,
        }
        return render(request, "articles/create.html", context)
    else:

        return redirect("articles:detail", pk)


@login_required
def delete(request, pk):
    articles = get_object_or_404(Article, pk=pk)
    if request.user == articles.user:
        articles.delete()
        return redirect("articles:index")
    else:
        return redirect("articles:index")


@login_required
def comments_create(request, article_pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            article = Article.objects.get(pk=article_pk)
            comment_form = ArticleCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.article = article
                comment.save()

                if not comment.user.profile.image:
                    comment_user_image = "/static/images/no-avatar.jpg"
                elif str(comment.user.profile.image)[:4] == "http":
                    comment_user_image = str(comment.user.profile.image)
                else:
                    comment_user_image = str(comment.user.profile.image.url)

                data = {
                    "pk": comment.pk,
                    "content": comment.content,
                    "userName": comment.user.profile.nickname,
                    "userPk": comment.user.pk,
                    "commentUserImage": comment_user_image,
                }
                return JsonResponse(data)
            return redirect("articles:detail", article_pk)
    return redirect("accounts:login")


@login_required
def comments_delete(request, comment_pk, article_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(ArticleComment, pk=comment_pk)
        is_deleted = False  # 삭제여부

        if request.user == comment.user:
            comment.delete()
            is_deleted = True  # 삭제여부
            data = {
                "is_deleted": is_deleted,
            }
            return JsonResponse(data)
    return redirect("articles:detail", article_pk)


def likes(request, article_pk):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=article_pk)
        if article.like.filter(pk=request.user.pk).exists():
            article.like.remove(request.user)
            is_liked = False
        else:
            article.like.add(request.user)
            is_liked = True
        data = {"is_liked": is_liked}
        return JsonResponse(data)
    return redirect("accounts:login")
