
from django.shortcuts import render,redirect,get_object_or_404
from .models import Article,ArticleComment, Image
from .forms import articleForm,ArticleCommentForm, ImageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import Profile
# Create your views here.


def home(request):
    # 파이썬이 주 언어인 사람 가져옴
    python = Profile.objects.filter(language = "Python")
    C = Profile.objects.filter(language = "C")
    Java = Profile.objects.filter(language = "Java")
    python_cnt = len(python)
    C_cnt = len(C)
    Java_cnt = len(Java)
    
    # 여기 고쳤음! 비율 계산시에 값이 0이면 ZeroDivisionError라는 친구를 만나게 됨!
    total_cnt = python_cnt + C_cnt + Java_cnt
    
    if total_cnt != 0 :
        # 비율 계산
        python_re=round((python_cnt/(python_cnt+Java_cnt+C_cnt))*100)
        C_re=round((C_cnt/(python_cnt+Java_cnt+C_cnt))*100)
        Java_re=round((Java_cnt/(python_cnt+Java_cnt+C_cnt))*100)

    python_re = 0
    C_re = 0
    Java_re= 0

    context = {
        'Python_re':python_re,
        'C_re':C_re,
        'Java_re':Java_re
      
    }
    return render(request, "articles/home.html", context)


def index(request):
    articles = Article.objects.all().order_by("-pk")
    context = {"articles": articles}
    return render(request, "articles/index.html", context)


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


@login_required
def detail(request, pk):
    articles = Article.objects.get(pk=pk)
    comment_form = ArticleCommentForm()
    context = {
        "articles": articles,
        "image_cnt": articles.image_set.count(),
        'comments':articles.articlecomment_set.all(),
        "comment_form":comment_form,
    }
    return render(request, "articles/detail.html", context)


@login_required
def update(request, pk):
    articles = get_object_or_404(Article, pk=pk)
    images = Image.objects.filter(article_id=pk)    # 기존 이미지

    if request.user == articles.user:
        if request.method == "POST":
            article_form = articleForm(request.POST, request.FILES, instance=articles)
            image_form = ImageForm(request.POST, request.FILES)
            tmp_images = request.FILES.getlist('image')

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

        return redirect("articles:detail",pk)
    
@login_required
def delete(request, pk):
    articles = get_object_or_404(Article, pk=pk)
    if request.user == articles.user:
        articles.delete()
        return redirect("articles:index")
    else:
        return redirect("articles:index")

@login_required
def comments_create(request,article_pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            article = Article.objects.get(pk=article_pk)
            comment_form = ArticleCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.article = article
                comment.save()
                data={
                    'pk':comment.pk,
                    'content':comment.content,
                    'userName':comment.user.username
                }
                return JsonResponse(data)
            return redirect('articles:detail',article_pk)
    return redirect('accounts:login')

@login_required
def comments_delete(request, comment_pk, article_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(ArticleComment, pk=comment_pk)
        is_deleted = False#삭제여부

        if request.user == comment.user:
            comment.delete()
            is_deleted = True#삭제여부
            data={
                "is_deleted":is_deleted,
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
        data={
            "is_liked":is_liked
        }
        return JsonResponse(data)
    return redirect('accounts:login')