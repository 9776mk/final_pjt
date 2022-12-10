from django.shortcuts import render
from .models import *
from .forms import *
from django.db.models import Q
from itertools import chain

# 체크박스
from django.views import generic

category_level = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]
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

# detail_category = {
#     "수학": [
#         "사칙연산",
#         "정수론",
#         "유클리드 호제법",
#         "확장 유클리드 호제법",
#         "소수 판정",
#         "에라토스테네스의 체",
#         "밀러-라빈 소수 판별법",
#         "모듈로 곱셈 역원",
#         "중국인의 나머지 정리",
#         "페르마의 소정리",
#         "오일러 피 함수",
#         "뫼비우스 반전 공식",
#         "폴라드 로",
#         "이산 로그",
#         "뤼카 정리",
#         "이산 제곱근",
#         "이산 k제곱근",
#         "조합론",
#         "번사이드 보조정리",
#         "확률론",
#         "기댓값의 선형성",
#         "선형대수학",
#         "가우스 소거법",
#         "미적분학",
#         "그린 정리",
#         "분할 정복을 이용한 거듭제곱",
#         "고속 푸리에 변환",
#         "다중 대입값 계산",
#         "수치해석",
#         "통계학",
#     ],
#     "구현": ["구현", "시뮬레이션"],
#     "다이나믹 프로그래밍": [
#         "다이나믹 프로그래밍",
#         "트리에서의 다이나믹 프로그래밍",
#         "비트필드를 이용한 다이나믹 프로그래밍",
#         "분할 정복을 사용한 최적화",
#         "커넥션 프로파일을 이용한 다이나믹 프로그래밍",
#         "덱을 이용한 다이나믹 프로그래밍",
#         "함수 개형을 이용한 최적화",
#         "커누스 최적화",
#         "단조 큐를 이용한 최적화",
#     ],
#     "그래프 이론": [
#         "그래프 이론",
#         "그래프 탐색",
#         "너비 우선 탐색",
#         "0-1 너비 우선 탐색",
#         "깊이 우선 탐색",
#         "다익스트라",
#         "A*",
#         "최소 스패닝 트리",
#         "플로이드-와샬",
#         "벨만-포드",
#         "위상 정렬",
#         "강한 연결 요소",
#         "2-SAT",
#         "단절점과 단절선",
#         "오일러 경로",
#         "선인장",
#         "평면 그래프",
#         "쌍대 그래프",
#         "스토어-바그너",
#         "양방향 탐색",
#         "유향 최소 신장 트리",
#         "현 그래프",
#         "차수열",
#     ],
#     "자료구조": [
#         "자료구조",
#         "큐",
#         "우선순위 큐",
#         "스택",
#         "연결 리스트",
#         "덱",
#         "세그먼트 트리",
#         "느리게 갱신되는 세그먼트 트리",
#         "퍼시스턴트 세그먼트 트리",
#         "다차원 세그먼트 트리",
#         "머지 소트 트리",
#         "분리 집합",
#         "해시를 사용한 집합과 맵",
#         "트리를 사용한 집합과 맵",
#         "희소 배열",
#     ],
#     "문자열": [
#         "문자열",
#         "파싱",
#         "UTF-8 입력 처리",
#         "KMP",
#         "라빈-카프",
#         "접미사 배열과 lcp 배열",
#         "정규 표현식",
#         "매내처",
#         "Z",
#         "로프",
#     ],
#     "그리디 알고리즘": ["그리디 알고리즘"],
#     "브루트포스 알고리즘": ["브루트포스 알고리즘"],
#     "정렬": ["정렬"],
#     "트리": [
#         "트리",
#         "최소 공통 조상",
#         "트라이",
#         "아호-코라식",
#         "접미사 트리",
#         "오일러 경로 테크닉",
#         "스플레이 트리",
#         "Heavy-Light 분할",
#         "센트로이드",
#         "센트로이드 분할",
#         "링크/컷 트리",
#         "트리 동형 사상",
#         "회문 트리",
#         "도미네이터 트리",
#         "트리 압축",
#         "탑 트리",
#         "레드-블랙 트리",
#     ],
#     "기타": ["기타"],
# }


def index(request):
    context = {
        "category_level": category_level,
        "category_": category_,
        # "tags": tags,
    }
    return render(request, "algorithm/index.html", context)


def search(request):
    # total = BJData_total.objects.all()
    # 선택된 레벨
    level = request.POST.getlist("level-btns")
    # 선택된 카테고리
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
    # for l in level:
    #     if l == "Bronze":
    #         total = chain(total, BJData_br.objects.all())
    #     elif l == "Silver":
    #         total = chain(total, BJData_si.objects.all())
    #     elif l == "Gold":
    #         total = chain(total, BJData_br.objects.all())
    #     elif l == "Platinum":
    #         total = chain(total, BJData_br.objects.all())
    #     elif l == "Diamond":
    #         total = chain(total, BJData_br.objects.all())
    #     elif l == "Ruby":
    #         total = chain(total, BJData_br.objects.all())
    # print(total)
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

    total = []
    for l in level:
        if l == "Bronze":
            br = BJData_br.objects.all()
            for j in category:
                filter_ = br.filter(Q(tags__icontains=j))
                total += list(filter_)
        elif l == "Silver":
            si = BJData_si.objects.all()
            for j in category:
                filter_ = si.filter(Q(tags__icontains=j))
                total += list(filter_)
        elif l == "Gold":
            go = BJData_go.objects.all()
            for j in category:
                filter_ = go.filter(Q(tags__icontains=j))
                total += list(filter_)
        elif l == "Platinum":
            pl = BJData_pl.objects.all()
            for j in category:
                filter_ = pl.filter(Q(tags__icontains=j))
                total += list(filter_)
        elif l == "Diamond":
            di = BJData_di.objects.all()
            for j in category:
                filter_ = di.filter(Q(tags__icontains=j))
                total += list(filter_)
        elif l == "Ruby":
            ru = BJData_ru.objects.all()
            for j in category:
                filter_ = ru.filter(Q(tags__icontains=j))
                total += list(filter_)

    # 중복된 태그가 있는 문제 제거
    total = set(total)

    context = {
        "search_list": total,
    }

    return render(request, "algorithm/search.html", context)
