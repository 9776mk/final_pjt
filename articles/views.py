
from django.shortcuts import render,redirect,get_object_or_404
from .models import Article,ArticleComment, Image
from .forms import articleForm,ArticleCommentForm, ImageForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, "articles/home.html")


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

    context = {
        "articles": articles,
        "image_cnt": articles.image_set.count(),
    }
    return render(request, "articles/detail.html", context)


@login_required
def update(request, pk):
    articles = get_object_or_404(Article, pk=pk)
    if request.user == articles.user:
        if request.method == "POST":
            article_form = articleForm(request.POST, request.FILES, instance=articles)
            if article_form.is_valid():
                article = article_form.save(commit=False)
                article.user = request.user
                article.save()
            return redirect("articles:detail", pk)
        else:
            article_form = articleForm(instance=articles)
        context = {
            "article_form": article_form,
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
            article = get_object_or_404(Article, pk=article_pk)
            comment_form = ArticleCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.article = article
                comment.save()
            return redirect("articles:detail", article.pk)
    return redirect('accounts:login')

@login_required
def comments_delete(request, comment_pk, article_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(ArticleComment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect("articles:detail", article_pk)

