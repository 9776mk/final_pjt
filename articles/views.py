from django.shortcuts import render,redirect,get_object_or_404
from .models import Article,ArticleComment
from .forms import articleForm,ArticleCommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    articles = Article.objects.all().order_by('-pk')
    context = {"articles":articles}
    return render(request, "articles/index.html",context)

@login_required
def create(request):
    if request.method == "POST":
        article_form = articleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        article_form = articleForm()
    context = {
        "article_form":article_form,
    }
    return render(request, "articles/create.html", context)
@login_required
def detail(request,article_pk):
    articles = Article.objects.get(pk=article_pk)
    context = {
        "articles":articles
    }
    return render(request, "articles/detail.html", context)
@login_required
def update(request,article_pk):
    articles = get_object_or_404(Article, pk=article_pk)
    if request.user == articles.user:
        if request.method == "POST":
            article_form = articleForm(request.POST, request.FILES ,instance=articles)
            if article_form.is_valid():
                article = article_form.save(commit=False)
                article.user = request.user
                article.save()
            return redirect('articles:detail',article_pk)
        else:
            article_form = articleForm(instance=articles)
        context={
            "article_form":article_form,
            "articles":articles,
        }
        return render(request, 'articles/create.html',context)
    else:
        return redirect("articles:detail",article_pk)
    
@login_required
def delete(request,article_pk):
    articles = get_object_or_404(Article, pk=pk)
    if request.user == articles.user:
        articles.delete()
        return redirect('articles:index')
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