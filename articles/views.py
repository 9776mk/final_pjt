from django.shortcuts import render,redirect,get_object_or_404
from .models import Article
from .forms import articleForm
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
def detail(request ,pk):
    articles = Article.objects.get(pk=pk)
    context = {
        "articles":articles
    }
    return render(request, "articles/detail.html", context)
@login_required
def update(request,pk):
    articles = get_object_or_404(Article, pk=pk)
    if request.user == articles.user:
        if request.method == "POST":
            article_form = articleForm(request.POST, request.FILES ,instance=articles)
            if article_form.is_valid():
                article = article_form.save(commit=False)
                article.user = request.user
                article.save()
            return redirect('articles:detail',pk)
        else:
            article_form = articleForm(instance=articles)
        context={
            "article_form":article_form,
            "articles":articles,
        }
        return render(request, 'articles/create.html',context)
    else:
        return redirect("articles:detail",pk)
@login_required
def delete(request,pk):
    articles = get_object_or_404(Article, pk=pk)
    if request.user == articles.user:
        articles.delete()
        return redirect('articles:index')
    else:
        return redirect("articles:index")