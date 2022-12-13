from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
import requests
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    studies = Study.objects.all().order_by("-pk")

    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(studies, 9)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "studies": page_obj,
        "max_index": max_index,
    }

    return render(request, "studies/index.html", context)


# 알고리즘 스터디
def index_al(request):
    studies = Study.objects.filter(category="알고리즘 공부").order_by("-pk")

    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(studies, 9)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "studies": page_obj,
        "max_index": max_index,
    }

    return render(request, "studies/index.html", context)


# 프론트엔드 스터디
def index_fe(request):
    studies = Study.objects.filter(category="프론트엔드 공부").order_by("-pk")

    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(studies, 9)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "studies": page_obj,
        "max_index": max_index,
    }

    return render(request, "studies/index.html", context)


# 백엔드 스터디
def index_be(request):
    studies = Study.objects.filter(category="백엔드 공부").order_by("-pk")

    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(studies, 9)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "studies": page_obj,
        "max_index": max_index,
    }

    return render(request, "studies/index.html", context)


# 기타 스터디
def index_etc(request):
    studies = Study.objects.filter(category="기타").order_by("-pk")

    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(studies, 9)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "studies": page_obj,
        "max_index": max_index,
    }

    return render(request, "studies/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        study_form = StudyForm(request.POST, request.FILES)

        if study_form.is_valid():
            study = study_form.save(commit=False)
            study.host_user = request.user
            study.save()

            List.objects.create(user=request.user, study=study, is_accepted=True)

            return redirect("studies:detail", study.pk)

    else:
        study_form = StudyForm()

    context = {
        "study_form": study_form,
    }

    return render(request, "studies/create.html", context)


def detail(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)
    waiting_list = List.objects.filter(study=study, is_accepted=False)
    accepted_list = List.objects.filter(study=study, is_accepted=True)

    waiting_user_list = waiting_list.values_list("user", flat=True)
    accepted_user_list = accepted_list.values_list("user", flat=True)

    # print(accepted_user_list) # user_pk 쿼리셋

    context = {
        "study": study,
        "waiting_list": waiting_list,
        "accepted_list": accepted_list,
        "waiting_user_list": waiting_user_list,
        "accepted_user_list": accepted_user_list,
    }

    return render(request, "studies/detail.html", context)


@login_required
def update(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    if request.user != study.host_user:
        return redirect("studies:index")

    if request.method == "POST":
        study_form = StudyForm(request.POST, request.FILES, instance=study)

        if study_form.is_valid():
            study = study_form.save(commit=False)
            study.host_user = request.user
            study.save()

            return redirect("studies:detail", study.pk)

    else:
        study_form = StudyForm(instance=study)

    context = {
        "study": study,
        "study_form": study_form,
        "study_pk": study_pk,
    }

    return render(request, "studies/update.html", context)


@login_required
def delete(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    if request.user == study.host_user and request.method == "POST":
        # 만약 스터디 인원이 있다면, 그 인원에게 알림
        study_members = List.objects.filter(study=study).values_list("user", flat=True)
        if study_members:
            for pk in study_members:
                member = get_object_or_404(get_user_model(), pk=pk)

                if member != study.host_user:
                    notice = f"'{request.user.profile.nickname}'님이 '{study.title}' 스터디를 삭제하였습니다."
                    StudyNotice.objects.create(
                        study_title=study.title, user=member, content=notice
                    )

        study.delete()

    return redirect("studies:index")


# 스터디 모집 마감 & 재모집 (방장)
@login_required
def close(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)
    accepted_cnt = List.objects.filter(study=study, is_accepted=True).count()

    if request.user == study.host_user and request.method == "POST":
        if study.is_closed == False:
            study.is_closed = True
            study.save()
            is_closed = True
            is_full = True if accepted_cnt == study.limit else False
        else:
            study.is_closed = False
            study.save()
            is_closed = False
            is_full = False

    data = {
        "is_closed": is_closed,
        "is_full": is_full,
    }

    # return redirect('studies:detail', study_pk)
    return JsonResponse(data)


# 스터디 가입 신청 및 취소 (방장 제외)
@login_required
def apply(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    is_closed = False
    is_applied = False

    if request.user != study.host_user and request.method == "POST":
        if study.is_closed == False:
            user_pks = List.objects.filter(is_accepted=False).values_list(
                "user", flat=True
            )

            # 아직 신청하지 않았으면, 유저를 List에 추가 (가입 신청)
            if not request.user.pk in user_pks:
                List.objects.create(user=request.user, study=study)

                # 방장에게 알림
                notice = f"'{request.user.profile.nickname}'님이 '{study.title}' 스터디에 가입을 신청하였습니다."
                StudyNotice.objects.create(
                    study_title=study.title, user=study.host_user, content=notice
                )
                is_applied = True

            # 이미 신청한 상태면, 유저를 List에서 삭제 (신청 취소)
            else:
                list_user = List.objects.get(user=request.user, study=study)
                list_user.delete()

                # 방장에게 알림
                notice = f"'{request.user.profile.nickname}'님이 '{study.title}' 스터디에 가입을 취소하였습니다."
                StudyNotice.objects.create(
                    study_title=study.title, user=study.host_user, content=notice
                )
                is_applied = False

            is_closed = False

        else:
            # messages.warning(request, '이미 모집이 마감된 스터디입니다.')
            is_closed = True

    data = {
        "is_closed": is_closed,
        "is_applied": is_applied,
    }

    # return redirect('studies:detail', study_pk)
    return JsonResponse(data)


# 스터디 가입 신청 수락 (방장)
@login_required
def accept(request, study_pk, user_pk):
    study = get_object_or_404(Study, pk=study_pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)

    is_full = False

    if request.user == study.host_user and request.method == "POST":
        accepted_list_cnt = List.objects.filter(study=study, is_accepted=True).count()

        # 정원이 다 차면, 모집 마감
        if study.limit == accepted_list_cnt:
            study.is_closed = True
            study.save()
            is_full = True

        else:
            # 해당 유저의 가입 승인 여부를 True로
            list_user = List.objects.get(user=user, study=study)
            list_user.is_accepted = True
            list_user.save()

        # 신청자에게 알림
        notice = f"'{study.title}' 스터디에 가입되었습니다."
        StudyNotice.objects.create(study_title=study.title, user=user, content=notice)

    # 수락한 유저의 프로필 이미지
    if not user.profile.image:
        user_image = "/static/images/no-avatar.jpg"
    elif str(user.profile.image)[:4] == "http":
        user_image = str(user.profile.image)
    else:
        user_image = str(user.profile.image.url)

    data = {
        "user_image": user_image,
        "user_nickname": user.profile.nickname,
        "user_username": user.username,
        "waiting_cnt": List.objects.filter(study=study, is_accepted=False).count(),
        "accepted_cnt": List.objects.filter(study=study, is_accepted=True).count(),
        "is_full": is_full,
    }

    # return redirect('studies:detail', study_pk)
    return JsonResponse(data)


# 스터디 가입 신청 거절 (방장)
@login_required
def deny(request, study_pk, user_pk):
    study = get_object_or_404(Study, pk=study_pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.user == study.host_user and request.method == "POST":
        list_user = List.objects.get(user=user, study=study)
        list_user.delete()

        # 신청자에게 알림
        notice = f"'{study.title}' 스터디 가입이 거절되었습니다."
        StudyNotice.objects.create(study_title=study.title, user=user, content=notice)

    data = {"waiting_cnt": List.objects.filter(study=study, is_accepted=False).count()}

    # return redirect('studies:detail', study_pk)
    return JsonResponse(data)


# 스터디 추방 (방장)
@login_required
def kick(request, study_pk, user_pk):
    study = get_object_or_404(Study, pk=study_pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.user == study.host_user and request.method == "POST":
        list_user = List.objects.get(user=user, study=study)
        list_user.delete()

        accepted_list_cnt = List.objects.filter(study=study, is_accepted=True).count()
        study.limit == accepted_list_cnt
        # study.is_closed = False
        study.save()

        # 신청자에게 알림
        notice = f"'{study.title}' 스터디에서 추방되었습니다."
        StudyNotice.objects.create(study_title=study.title, user=user, content=notice)

    data = {
        "accepted_cnt": List.objects.filter(study=study, is_accepted=True).count(),
    }

    # return redirect('studies:detail', study_pk)
    return JsonResponse(data)


# 스터디 탈퇴 (방장 제외)
@login_required
def withdraw(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    if request.user != study.host_user and request.method == "POST":
        list_user = List.objects.get(user=request.user, study=study)
        list_user.delete()

        accepted_list_cnt = List.objects.filter(study=study, is_accepted=True).count()
        study.limit == accepted_list_cnt
        # study.is_closed = False
        study.save()

        # 방장에게 알림
        notice = f"'{request.user.profile.nickname}'님이 '{study.title}' 스터디에서 탈퇴하였습니다."
        StudyNotice.objects.create(
            study_title=study.title, user=study.host_user, content=notice
        )

    data = {
        "accepted_cnt": List.objects.filter(study=study, is_accepted=True).count(),
    }

    # return redirect('studies:detail', study_pk)
    return JsonResponse(data)


# 알림 삭제
@login_required
def notice_delete(request, notice_pk):
    is_deleted = False

    if request.user.is_authenticated and request.method == "POST":
        notice = get_object_or_404(StudyNotice, pk=notice_pk)
        notice.delete()
        is_deleted = True

    data = {
        "is_deleted": is_deleted,
    }

    # return redirect('home')
    return JsonResponse(data)


# 알림 전체 삭제
@login_required
def notice_delete_all(request):
    is_deleted = False

    if request.user.is_authenticated and request.method == "POST":
        notices = StudyNotice.objects.filter(user=request.user)
        for notice in notices:
            notice.delete()

        is_deleted = True

    data = {
        "is_deleted": is_deleted,
    }

    # return redirect('home')
    return JsonResponse(data)


# 스터디 게시판 인덱스
def board_index(request, study_pk):
    page = request.GET.get("page", "1")  # 페이지
    study = get_object_or_404(Study, pk=study_pk)
    boards = Board.objects.filter(study_id=study_pk).order_by("-pk")
    paginator = Paginator(boards, 15)  # 페이지당 15개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)  # 마지막 페이지 번호
    # print(boards)

    context = {
        "study": study,
        "boards": boards,
        "articles": page_obj,
        "max_index": max_index,
    }
    return render(request, "studies/board_index.html", context)


def board_index_1(request, study_pk):
    articles = Board.objects.filter(category="문제").order_by("-pk")
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(articles, 15)  # 페이지당 15개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)  # 마지막 페이지 번호

    context = {
        "articles": page_obj,
        "max_index": max_index,
    }
    return render(request, "articles/index.html", context)


def board_index_2(request):
    articles = Board.objects.filter(category="질문").order_by("-pk")
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(articles, 15)  # 페이지당 15개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)  # 마지막 페이지 번호

    context = {
        "articles": page_obj,
        "max_index": max_index,
    }
    return render(request, "articles/index.html", context)


def board_index_3(request):
    articles = Board.objects.filter(category="잡담").order_by("-pk")
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(articles, 15)  # 페이지당 15개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)  # 마지막 페이지 번호

    context = {
        "articles": page_obj,
        "max_index": max_index,
    }
    return render(request, "articles/index.html", context)


# 스터디 게시판 게시물 생성
@login_required
def board_create(request, study_pk):
    if request.method == "POST":
        study = Study.objects.get(pk=study_pk)
        Board_Form = BoardForm(request.POST)
        # print(Board_Form.is_valid())

        if Board_Form.is_valid():
            board = Board_Form.save(commit=False)
            board.study = study
            board.user = request.user
            board.save()

            return redirect("studies:board_index", study_pk)

    else:
        Board_Form = BoardForm()

    context = {
        "study_pk": study_pk,
        "Board_Form": Board_Form,
    }
    return render(request, "studies/board_create.html", context)


# 스터디 게시판 상세보기
def board_detail(request, study_pk, article_pk):
    # comment = Comment.objects.get(pk=comment_pk)
    # comment_form = CommentForm()
    study = get_object_or_404(Study, pk=study_pk)
    accepted_list = List.objects.filter(study=study, is_accepted=True)
    boards = Board.objects.get(pk=article_pk)

    # 백준 아이디 저장할 리스트
    boj_id = []
    # 스터디에 가입된 사람들 중
    for i in accepted_list:
        # 백준 아이디가 있다면
        if i.user.profile.boj_id:
            id = i.user.profile.boj_id
            # 백준 아이디가 푼 문제들을 solved_problems에 저장
            solved_problems = []
            page_num = 1
            while True:
                url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{id}&page={page_num}"
                r_solved = requests.get(url)
                ################ 백준 api 사용 제한이 있어서 많이 사용하는 경우 아래 코드를 못 받아옴 ################
                ###### try를 사용해야 할 듯 ###########
                solved = json.loads(r_solved.content.decode("utf-8"))

                items = solved.get("items")

                if items:
                    for item in items:
                        solved_problems.append(item.get("problemId"))
                    page_num += 1
                else:
                    break
            # print(solved_problems)
            # print(boards.problem_number)
            # print(boards.problem_number in solved_problems)

            ###### 백준 api 때문에 막혀서 잠시 주석 처리
            if boards.problem_number in solved_problems:
                boj_id.append({i.user.profile.boj_id: True})
            else:
                boj_id.append({i.user.profile.boj_id: False})

    print(boj_id)
    print(type(boj_id))  # 리스트
    print(type(boj_id[0]))  # 딕셔너리

    for i in boj_id:
        print(i.keys())  # dict_keys(['9776mk'])
        print(i.values())  # dict_values([False])

    context = {
        # "comment": comment,
        # "comment_form": comment_form,
        "boards": boards,
        "accepted_list": accepted_list,
        "problem_check": boj_id,
    }
    return render(request, "studies/board_detail.html", context)


def problem_check(request):
    is_valid = False
    url = "https://www.acmicpc.net/problem/"
    id = json.loads(request.body).get("problem_num")
    print(id)

    if id:
        response = requests.get(url + id)
        if response.status_code == 200:
            is_valid = True

    data = {
        "is_valid": is_valid,
    }

    return JsonResponse(data)


# 알림 읽음
@login_required
def notice_read(request):
    is_read = False

    if request.user.is_authenticated and request.method == "POST":
        notices = StudyNotice.objects.filter(user=request.user, read=False)
        for notice in notices:
            notice.read = True
            notice.save()

        is_read = True

    data = {
        "is_read": is_read,
    }

    # return redirect('home')
    return JsonResponse(data)
