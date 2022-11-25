from django.shortcuts import render,redirect

# Create your views here.

def index(request):

    return render(request, "articles/index.html")
def create(request):
    
    return render(request, "articles/create.html")
def detail(request):
    
    return render(request, "articles/detail.html")
# def update(request):
    
#     return redirect("articles:detail")
# def delete(request):
    
#     return redirect("articles:index")