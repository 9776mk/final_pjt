from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.index, name="index"),
    path("index_al/", views.index_al, name="index_al"),
    path("index_fe/", views.index_fe, name="index_fe"),
    path("index_be/", views.index_be, name="index_be"),
    path("index_etc/", views.index_etc, name="index_etc"),
    path("create/", views.create, name="create"),
    path("<int:study_pk>/", views.detail, name="detail"),
    path("<int:study_pk>/board/", views.board, name="board"),
    path("<int:study_pk>/update/", views.update, name="update"),
    path("<int:study_pk>/delete/", views.delete, name="delete"),
    path("<int:study_pk>/close/", views.close, name="close"),  # 모집 마감 & 재모집 (방장만)
    path("<int:study_pk>/apply/", views.apply, name="apply"),  # 가입 신청 & 취소 (방장 제외)
    path("<int:study_pk>/user/<int:user_pk>/accept/", views.accept, name="accept"),  # 신청 수락 (방장)
    path("<int:study_pk>/user/<int:user_pk>/deny/", views.deny, name="deny"),  # 신청 거절 (방장)
    path("<int:study_pk>/user/<int:user_pk>/kick/", views.kick, name="kick"),  # 스터디 추방 (방장)
    path("<int:study_pk>/withdraw/", views.withdraw, name="withdraw"),  # 스터디 탈퇴 (방장 제외)
    path("<int:notice_pk>/notice_delete/", views.notice_delete, name="notice_delete"),  # 알림 삭제
    path("notice_read/", views.notice_read, name="notice_read"),    # 알림 읽음
]
