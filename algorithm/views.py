from django.shortcuts import render
from .models import *
from .forms import *
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator

# 체크박스
from django.views import generic

category_level = {
    "Bronze": "br",
    "Silver": "si",
    "Gold": "go",
    "Platinum": "pl",
    "Diamond": "di",
    "Ruby": "ru",
}
category_ = [
    "수학",
    "구현",
    "정렬",
    "자료구조",
    "다이나믹 프로그래밍",
    "그래프 이론",
    "문자열",
    "그리디",
    "브루트포스",
    "트리",
]


def index(request):
    context = {
        "category_level": category_level,
        "category_": category_,
        # "tags": tags,
    }
    return render(request, "algorithm/index.html", context)


def search(request):
    # 선택된 레벨
    level = request.GET.getlist("level-btns")
    # # 레벨을 db 이름 리스트로 변환
    level_ = []
    for i in level:
        level_.append(category_level.get(i))
    # print(level_)

    # 선택된 카테고리
    category = request.GET.getlist("category-btns")
    # 검색어
    search = request.GET.get("search", "")
    total = []

    # 검색어가 있는 경우
    if search:
        total_ = BJData_total.objects.all()
        filter_ = total_.filter(
            Q(title__icontains=search)
            | Q(number__icontains=search)
            | Q(tags__icontains=search)
        )
        total += list(filter_)

    # 검색어가 없는 경우
    else:
        # 레벨 O
        if level:
            for l in level_:
                if l == "br":
                    br = BJData_br.objects.all()
                    # 카테고리 O
                    if category:
                        for c in category:
                            # 검색어 O
                            filter_ = br.filter(Q(tags__icontains=c))
                            total += list(filter_)
                    # 카테고리 X
                    else:
                        total += list(br)
                if l == "si":
                    si = BJData_si.objects.all()
                    # 카테고리 O
                    if category:
                        for c in category:
                            # 검색어 O
                            filter_ = si.filter(Q(tags__icontains=c))
                            total += list(filter_)
                    # 카테고리 X
                    else:
                        total += list(si)
                if l == "go":
                    go = BJData_go.objects.all()
                    # 카테고리 O
                    if category:
                        for c in category:
                            # 검색어 O
                            filter_ = go.filter(Q(tags__icontains=c))
                            total += list(filter_)
                    # 카테고리 X
                    else:
                        total += list(go)
                if l == "pl":
                    pl = BJData_pl.objects.all()
                    # 카테고리 O
                    if category:
                        for c in category:
                            # 검색어 O
                            filter_ = pl.filter(Q(tags__icontains=c))
                            total += list(filter_)
                    # 카테고리 X
                    else:
                        total += list(pl)
                if l == "di":
                    di = BJData_di.objects.all()
                    # 카테고리 O
                    if category:
                        for c in category:
                            # 검색어 O
                            filter_ = di.filter(Q(tags__icontains=c))
                            total += list(filter_)
                    # 카테고리 X
                    else:
                        total += list(di)
                if l == "ru":
                    ru = BJData_ru.objects.all()
                    # 카테고리 O
                    if category:
                        for c in category:
                            # 검색어 O
                            filter_ = ru.filter(Q(tags__icontains=c))
                            total += list(filter_)
                    # 카테고리 X
                    else:
                        total += list(ru)

        # 레벨 X
        else:
            total_ = BJData_total.objects.all()
            # 카테고리 O
            if category:
                for c in category:
                    filter_ = total_.filter(Q(tags__icontains=c))
                    total += list(filter_)
            # 카테고리 X

    # 중복된 태그가 있는 문제 제거
    total = set(total)
    # print(total)
    result = []
    for t in total:
        num = t.number
        title = t.title
        lev = t.level
        t = t.tags
        ts = t.replace("[", "")
        ts = ts.replace("]", "")
        ts = ts.replace("'", "")
        ts = ts.replace(", ", " #")
        result.append((num, title, ts, lev))

    # 페이지네이션
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(result, 15)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    # 선택된 카테고리
    is_selected_lev = True if level else False
    is_selected_cate = True if category else False
    is_selected_input = True if search else False

    # print(is_selected_lev, is_selected_cate, is_selected_input)
    # print(level, category, search)
    # # print(result)
    # print(not level and not category)

    context = {
        "search": search, 
        "results": page_obj,
        "max_index": max_index,
        "level": level,
        "category": category,
        "search": search,
        "is_selected_lev": is_selected_lev,
        "is_selected_cate": is_selected_cate,
        "is_selected_input": is_selected_input,
    }

    return render(request, "algorithm/search.html", context)
