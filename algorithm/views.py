from django.shortcuts import render
from .models import *
from .forms import *
from django.db.models import Q
from itertools import chain

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
    level = request.POST.getlist("level-btns")
    # # 레벨을 db 이름 리스트로 변환
    level_ = []
    for i in level:
        level_.append(category_level.get(i))
    # print(level_)

    # 선택된 카테고리
    category = request.POST.getlist("category-btns")
    # 검색어
    search = request.POST.get("search", "")
    total = []

    # 난이도 선택
    if level:
        # 각각의 난이도에 해당하는 DB 불러오기
        for l in level_:
            if l == "br":
                br = BJData_br.objects.all()
                # 카테고리 선택(태그)
                if category:
                    for c in category:
                        # 검색어 O
                        if search:
                            filter_ = br.filter(
                                Q(title__icontains=search)
                                | Q(number__icontains=search)
                                | Q(tags__icontains=search)
                                | Q(tags__icontains=c)
                            )
                            total += list(filter_)
                        # 검색어 X
                        else:
                            filter_ = br.filter(Q(tags__icontains=c))
                            total += list(filter_)

                # 카테고리 X
                else:
                    # 검색어 O
                    if search:
                        filter_ = br.filter(
                            Q(title__icontains=search)
                            | Q(number__icontains=search)
                            | Q(tags__icontains=search)
                        )
                        total += list(filter_)

                    # 검색어 X
                    else:
                        filter_ = BJData_br.objects.all()
                        total += list(filter_)

            elif l == "si":
                si = BJData_si.objects.all()
                # 카테고리 선택(태그)
                if category:
                    for c in category:
                        # 검색어 O
                        if search:
                            filter_ = si.filter(
                                Q(title__icontains=search)
                                | Q(number__icontains=search)
                                | Q(tags__icontains=search)
                                | Q(tags__icontains=c)
                            )
                            total += list(filter_)
                        # 검색어 X
                        else:
                            filter_ = si.filter(Q(tags__icontains=c))
                            total += list(filter_)

                # 카테고리 X
                else:
                    # 검색어 O
                    if search:
                        filter_ = si.filter(
                            Q(title__icontains=search)
                            | Q(number__icontains=search)
                            | Q(tags__icontains=search)
                        )
                        total += list(filter_)

                    # 검색어 X
                    else:
                        filter_ = BJData_si.objects.all()
                        total += list(filter_)
            elif l == "go":
                go = BJData_go.objects.all()
                # 카테고리 선택(태그)
                if category:
                    for c in category:
                        # 검색어 O
                        if search:
                            filter_ = go.filter(
                                Q(title__icontains=search)
                                | Q(number__icontains=search)
                                | Q(tags__icontains=search)
                                | Q(tags__icontains=c)
                            )
                            total += list(filter_)
                        # 검색어 X
                        else:
                            filter_ = go.filter(Q(tags__icontains=c))
                            total += list(filter_)

                # 카테고리 X
                else:
                    # 검색어 O
                    if search:
                        filter_ = go.filter(
                            Q(title__icontains=search)
                            | Q(number__icontains=search)
                            | Q(tags__icontains=search)
                        )
                        total += list(filter_)

                    # 검색어 X
                    else:
                        filter_ = BJData_go.objects.all()
                        total += list(filter_)
            elif l == "pl":
                pl = BJData_pl.objects.all()
                # 카테고리 선택(태그)
                if category:
                    for c in category:
                        # 검색어 O
                        if search:
                            filter_ = pl.filter(
                                Q(title__icontains=search)
                                | Q(number__icontains=search)
                                | Q(tags__icontains=search)
                                | Q(tags__icontains=c)
                            )
                            total += list(filter_)
                        # 검색어 X
                        else:
                            filter_ = pl.filter(Q(tags__icontains=c))
                            total += list(filter_)

                # 카테고리 X
                else:
                    # 검색어 O
                    if search:
                        filter_ = pl.filter(
                            Q(title__icontains=search)
                            | Q(number__icontains=search)
                            | Q(tags__icontains=search)
                        )
                        total += list(filter_)

                    # 검색어 X
                    else:
                        filter_ = BJData_pl.objects.all()
                        total += list(filter_)
            elif l == "di":
                di = BJData_di.objects.all()
                # 카테고리 선택(태그)
                if category:
                    for c in category:
                        # 검색어 O
                        if search:
                            filter_ = di.filter(
                                Q(title__icontains=search)
                                | Q(number__icontains=search)
                                | Q(tags__icontains=search)
                                | Q(tags__icontains=c)
                            )
                            total += list(filter_)
                        # 검색어 X
                        else:
                            filter_ = di.filter(Q(tags__icontains=c))
                            total += list(filter_)

                # 카테고리 X
                else:
                    # 검색어 O
                    if search:
                        filter_ = di.filter(
                            Q(title__icontains=search)
                            | Q(number__icontains=search)
                            | Q(tags__icontains=search)
                        )
                        total += list(filter_)

                    # 검색어 X
                    else:
                        filter_ = BJData_di.objects.all()
                        total += list(filter_)
            elif l == "ru":
                ru = BJData_ru.objects.all()
                # 카테고리 선택(태그)
                if category:
                    for c in category:
                        # 검색어 O
                        if search:
                            filter_ = ru.filter(
                                Q(title__icontains=search)
                                | Q(number__icontains=search)
                                | Q(tags__icontains=search)
                                | Q(tags__icontains=c)
                            )
                            total += list(filter_)
                        # 검색어 X
                        else:
                            filter_ = ru.filter(Q(tags__icontains=c))
                            total += list(filter_)

                # 카테고리 X
                else:
                    # 검색어 O
                    if search:
                        filter_ = ru.filter(
                            Q(title__icontains=search)
                            | Q(number__icontains=search)
                            | Q(tags__icontains=search)
                        )
                        total += list(filter_)

                    # 검색어 X
                    else:
                        filter_ = BJData_ru.objects.all()
                        total += list(filter_)
    # 난이도 선택 X
    else:
        total_ = BJData_total.objects.all()
        # 카테고리 O
        if category:
            for c in category:
                # 검색어 O
                if search:
                    filter_ = total_.filter(
                        Q(title__icontains=search)
                        | Q(number__icontains=search)
                        | Q(tags__icontains=search)
                        | Q(tags__icontains=c)
                    )
                    total += list(filter_)
            # 검색어가 없을 때
            else:
                filter_ = total_.filter(Q(tags__icontains=c))
                total += list(filter_)
        # 카테고리 X
        else:
            # 검색어가 있을 때
            if search:
                filter_ = total_.filter(
                    Q(title__icontains=search)
                    | Q(number__icontains=search)
                    | Q(tags__icontains=search)
                )
                total += list(filter_)
            # 검색어가 없을 때
            else:
                pass

    # # 난이도 선택
    # if level:
    #     # 각각의 난이도에 해당하는 DB 불러오기
    #     for l in level_:
    #         if l == 'br':
    #             br = BJData_br.objects.all()
    #             # 카테고리 선택(태그)
    #             if category:
    #                 for c in category:
    #                     # 검색어가 있을 때
    #                     if search:
    #                         filter_ = br.filter(Q(title__icontains=search) | Q(number__icontains=search) | Q(tags__icontains=c))
    #                         total += list(filter_)
    #                     # 검색어가 없을 때
    #                     else:
    #                         filter_ = br.filter(Q(tags__icontains=c))
    #                         total += list(filter_)

    #             # 카테고리 X
    #             else:
    #                 # 검색어가 있을 때
    #                 if search:
    #                     filter_ = br.filter(Q(title__icontains=search) | Q(number__icontains=search) | Q(tags__icontains=search))
    #                     total += list(filter_)

    #                 # 검색어가 없을 때
    #                 else:
    #                     filter_ = BJData_br.objects.all()
    #                     total += list(filter_)
    # # 난이도 선택 X
    # else:
    #     # 카테고리가 선택되었을 때
    #     if category:

    #         # 검색어가 있을 때
    #         if search:

    #         # 검색어가 없을 때
    #         else:

    #     # 카테고리가 선택되지 않았을 때
    #     else:
    #         # 검색어가 있을 때
    #         if search:

    #         # 검색어가 없을 때
    #         else:

    # # 난이도가 선택되지 않았을 때
    # else:
    #     # 카테고리가 선택되었을 때
    #     if category:

    #         # 검색어가 있을 때
    #         if search:

    #         # 검색어가 없을 때
    #         else:

    #     # 카테고리가 선택되지 않았을 때
    #     else:
    #         # 검색어가 있을 때
    #         if search:

    #         # 검색어가 없을 때
    #         else:

    # 검색어가 있을 때
    # if search:
    #     for l in level:
    #         if l == "Bronze":
    #             br = BJData_br.objects.all()
    #             for j in category:
    #                 filter_ = br.filter(Q(tags__icontains=j))
    #                 total += list(filter_)
    #         elif l == "Silver":
    #             si = BJData_si.objects.all()
    #             for j in category:
    #                 filter_ = si.filter(Q(tags__icontains=j))
    #                 total += list(filter_)
    #         elif l == "Gold":
    #             go = BJData_go.objects.all()
    #             for j in category:
    #                 filter_ = go.filter(Q(tags__icontains=j))
    #                 total += list(filter_)
    #         elif l == "Platinum":
    #             pl = BJData_pl.objects.all()
    #             for j in category:
    #                 filter_ = pl.filter(Q(tags__icontains=j))
    #                 total += list(filter_)
    #         elif l == "Diamond":
    #             di = BJData_di.objects.all()
    #             for j in category:
    #                 filter_ = di.filter(Q(tags__icontains=j))
    #                 total += list(filter_)
    #         elif l == "Ruby":
    #             ru = BJData_ru.objects.all()
    #             for j in category:
    #                 filter_ = ru.filter(Q(tags__icontains=j))
    #                 total += list(filter_)
    # # 검색어가 없을 때
    # else:
    #     for l in level:
    #         # 카테고리가 선택된 경우
    #         if category:
    #             if l == "Bronze":
    #                 br = BJData_br.objects.all()
    #                 for j in category:
    #                     filter_ = br.filter(Q(tags__icontains=j))
    #                     total += list(filter_)
    #             elif l == "Silver":
    #                 si = BJData_si.objects.all()
    #                 for j in category:
    #                     filter_ = si.filter(Q(tags__icontains=j))
    #                     total += list(filter_)
    #             elif l == "Gold":
    #                 go = BJData_go.objects.all()
    #                 for j in category:
    #                     filter_ = go.filter(Q(tags__icontains=j))
    #                     total += list(filter_)
    #             elif l == "Platinum":
    #                 pl = BJData_pl.objects.all()
    #                 for j in category:
    #                     filter_ = pl.filter(Q(tags__icontains=j))
    #                     total += list(filter_)
    #             elif l == "Diamond":
    #                 di = BJData_di.objects.all()
    #                 for j in category:
    #                     filter_ = di.filter(Q(tags__icontains=j))
    #                     total += list(filter_)
    #             elif l == "Ruby":
    #                 ru = BJData_ru.objects.all()
    #                 for j in category:
    #                     filter_ = ru.filter(Q(tags__icontains=j))
    #                     total += list(filter_)
    #         else:
    #             if l == "Bronze":
    #                 total += list(BJData_br.objects.all())
    #             elif l == "Silver":
    #                 total += list(BJData_si.objects.all())
    #             elif l == "Gold":
    #                 total += list(BJData_go.objects.all())
    #             elif l == "Platinum":
    #                 total += list(BJData_pl.objects.all())
    #             elif l == "Diamond":
    #                 total += list(BJData_di.objects.all())
    #             elif l == "Ruby":
    #                 total += list(BJData_ru.objects.all())

    # 중복된 태그가 있는 문제 제거
    total = set(total)

    context = {"search": search, "category_list": total}

    return render(request, "algorithm/search.html", context)
