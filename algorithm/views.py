from django.shortcuts import render
from .models import *
from .forms import *
from django.db.models import Q
from itertools import chain

# 체크박스
from django.views import generic


def index(request):
    br = BJData_br.objects.all()
    si = BJData_si.objects.all()
    go = BJData_go.objects.all()
    pl = BJData_pl.objects.all()
    di = BJData_di.objects.all()
    ru = BJData_ru.objects.all()

    category_level = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]
    category_ = [
        "수학",
        "구현",
        "다이나믹 프로그래밍",
        "그래프 이론",
        "자료구조",
        "문자열",
        "그리디",
        "브루트포스",
        "정렬",
        "기하학",
        "트리",
        "이분 탐색",
        "애드 혹",
        "재귀",
        "투 포인터",
        "백 트래킹",
    ]

    context = {
        "br": br,
        "si": si,
        "go": go,
        "pl": pl,
        "di": di,
        "ru": ru,
        "category_level": category_level,
        "category_": category_,
        # "tags": tags,
    }
    return render(request, "algorithm/index.html", context)


def search(request):
    # br = BJData_br.objects.order_by("pk")
    # search = request.GET.get("search")

    # if search:
    #     search_list = br.filter(
    #         Q(title__icontains=search)
    #         | Q(number__icontains=search)
    #         | Q(tags__icontains=search)
    #     )
    #     context = {
    #         "search": search,
    #         "search_list": search_list,
    #     }
    # else:
    #     context = {
    #         "search": search,
    #         "search_list": br,
    #     }
    # 리스트 형태로 받아옴

    # total = list(BJData_total.objects.all())
    total = BJData_total.objects.all()

    level = request.POST.getlist("level-btns")
    category = request.POST.getlist("category-btns")

    # 1. UNION 사용
    # for l in level:
    #     if l == "Bronze":
    #         total = total.union(BJData_br.objects.all())
    #     elif l == "Silver":
    #         total = total.union(BJData_si.objects.all())
    #     elif l == "Gold":
    #         total = total.union(BJData_go.objects.all())
    #     elif l == "Platinum":
    #         total = total.union(BJData_pl.objects.all())
    #     elif l == "Diamond":
    #         total = total.union(BJData_di.objects.all())
    #     elif l == "Ruby":
    #         total = total.union(BJData_ru.objects.all())
    # Calling QuerySet.filter() after union() is not supported. 오류 발생
    # In addition, only LIMIT, OFFSET, COUNT(*), ORDER BY, and specifying columns (i.e. slicing, count(), order_by(), and values()/values_list()) 만 사용 가능
    # total = total.values_list("tags")

    # 2. 리스트로 변환 후 쿼리셋으로 다시 변환 불가
    # total = list(BJData_total.objects.all())
    # for l in level:
    #     if l == "Bronze":
    #         # print(list(BJData_br.objects.all()))
    #         total = total + list(BJData_br.objects.all())
    #         # print(total)
    #     elif l == "Silver":
    #         total = total + list(BJData_si.objects.all())
    #     elif l == "Gold":
    #         total = total + list(BJData_go.objects.all())
    #     elif l == "Platinum":
    #         total = total + list(BJData_pl.objects.all())
    #     elif l == "Diamond":
    #         total = total + list(BJData_di.objects.all())
    #     elif l == "Ruby":
    #         total = total + list(BJData_ru.objects.all())

    # 3. chain 사용
    for l in level:
        if l == "Bronze":
            total = chain(total, BJData_br.objects.all())
        elif l == "Silver":
            total = chain(total, BJData_si.objects.all())
        elif l == "Gold":
            total = chain(total, BJData_br.objects.all())
        elif l == "Platinum":
            total = chain(total, BJData_br.objects.all())
        elif l == "Diamond":
            total = chain(total, BJData_br.objects.all())
        elif l == "Ruby":
            total = chain(total, BJData_br.objects.all())
    print(total)
    # 'itertools.chain' object has no attribute 'filter'
    # https://docs.python.org/ko/3/library/itertools.html

    # 4. or 사용
    # for l in level:
    #     if l == "Bronze":
    #         total = total | BJData_br.objects.all()
    #     elif l == "Silver":
    #         total = total | BJData_si.objects.all()
    #     elif l == "Gold":
    #         total = total | BJData_br.objects.all()
    #     elif l == "Platinum":
    #         total = total | BJData_br.objects.all()
    #     elif l == "Diamond":
    #         total = total | BJData_br.objects.all()
    #     elif l == "Ruby":
    #         total = total | BJData_br.objects.all()
    # # 오류 : Cannot combine queries on two different base models.
    # print(total)

    for j in category:
        total = total.filter(tags=j)
        print(total)

    context = {
        "search_list": total,
    }

    return render(request, "algorithm/search.html", context)
