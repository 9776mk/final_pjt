from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:study_pk>/", views.detail, name="detail"),
    path("<int:study_pk>/board/", views.board, name="board"),  # 스터디 전용 게시판
    path(
        "<int:study_pk>/board/create/", views.board_create, name="board_create"
    ),  # 스터디 게시판 글 작성
    path(
        "<int:study_pk>/board/<int:article_pk>/",
        views.board_detail,
        name="board_detail",
    ),  # 스터디 게시판 글 보기
    path("problem_check/", views.problem_check, name="problem_check"),  # 백준 문제 확인
    path("<int:study_pk>/update/", views.update, name="update"),
    path("<int:study_pk>/delete/", views.delete, name="delete"),
    path("<int:study_pk>/close/", views.close, name="close"),  # 모집 마감 & 재모집 (방장만)
    path("<int:study_pk>/apply/", views.apply, name="apply"),  # 가입 신청 & 취소 (방장 제외)
    path(
        "<int:study_pk>/user/<int:user_pk>/accept/", views.accept, name="accept"
    ),  # 신청 수락 (방장)
    path(
        "<int:study_pk>/user/<int:user_pk>/deny/", views.deny, name="deny"
    ),  # 신청 거절 (방장)
    path(
        "<int:study_pk>/user/<int:user_pk>/kick/", views.kick, name="kick"
    ),  # 스터디 추방 (방장)
    path("<int:study_pk>/withdraw/", views.withdraw, name="withdraw"),  # 스터디 탈퇴 (방장 제외)
    path(
        "<int:notice_pk>/notice_delete/", views.notice_delete, name="notice_delete"
    ),  # 알림 삭제
]
