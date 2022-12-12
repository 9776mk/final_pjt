from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def index(request):
    studies = Study.objects.all()

    context = {
        "studies": studies,
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
            user_pks = List.objects.values_list("user", flat=True)

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

    if request.user == study.host_user and request.method == "POST":
        if study.is_closed == False:
            # 해당 유저의 가입 승인 여부를 True로
            list_user = List.objects.get(user=user, study=study)
            list_user.is_accepted = True
            list_user.save()

            # 수락 후 정원이 다 차면, 모집 마감
            accepted_list_cnt = List.objects.filter(
                study=study, is_accepted=True
            ).count()
            if study.limit == accepted_list_cnt:
                study.is_closed = True
                study.save()

            # 신청자에게 알림
            notice = f"'{study.title}' 스터디에 가입되었습니다."
            StudyNotice.objects.create(
                study_title=study.title, user=user, content=notice
            )

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


def board(request, pk):
    return render(request, "studies/board.html")
