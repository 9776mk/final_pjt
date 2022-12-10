from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
import random


# Create your views here.
def index(request):
    users = get_user_model().objects.all()
    category_langs = ["Python", "Java", "C", "C++", "JavaScript", "PHP"]
    category_mbtis = [
        "ISTJ",
        "ISFJ",
        "ISTP",
        "ISFP",
        "INFJ",
        "INTJ",
        "INFP",
        "INTP",
        "ESTJ",
        "ESFJ",
        "ESTP",
        "ESFP",
        "ENFJ",
        "ENTJ",
        "ENFP",
        "ENTP",
    ]

    context = {
        "users": users,
        "category_langs": category_langs,
        "category_mbtis": category_mbtis,
    }

    return render(request, "friends/index.html", context)


def recommend(request):
    users = get_user_model().objects.all()

    # 랜덤 추천
    num_total_users = get_user_model().objects.count()
    input_num = int(request.POST.get("num-of-people"))
    warning = ""

    if input_num > num_total_users:
        input_num = num_total_users
        warning = "입력하신 숫자가 개발자의 숫자보다 큽니다."

    recommended_users = random.sample(list(users), input_num)

    context = {
        "warning": warning,
        "recommended_users": recommended_users,
    }

    return render(request, "friends/recommend.html", context)
