from django.shortcuts import render
from django.contrib.auth import get_user_model


# Create your views here.
def index(request):
    users = get_user_model().objects.all()
    category_langs = ['Python', 'Java', 'C', 'C++', 'JavaScript', 'PHP']
    category_mbtis = [
        'ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP',
        'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ', 'ESTP', 'ESFP', 'ENFP', 'ENTP',
    ]

    context = {
        'users': users,
        'category_langs': category_langs,
        'category_mbtis': category_mbtis,
    }

    return render(request, 'friends/index.html', context)