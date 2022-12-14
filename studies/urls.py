from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.index, name="index"),
    path("problem_check/", views.problem_check, name="problem_check"),  # 백준 문제 확인
    path("index_al/", views.index_al, name="index_al"),
    path("index_fe/", views.index_fe, name="index_fe"),
    path("index_be/", views.index_be, name="index_be"),
    path("index_etc/", views.index_etc, name="index_etc"),
    path("create/", views.create, name="create"),
    path("<int:study_pk>/", views.detail, name="detail"),
    path("<int:study_pk>/update/", views.update, name="update"),
    path("<int:study_pk>/delete/", views.delete, name="delete"),
    path("<int:study_pk>/close/", views.close, name="close"),  # 모집 마감 & 재모집 (방장만)
    path("<int:study_pk>/apply/", views.apply, name="apply"),  # 가입 신청 & 취소 (방장 제외)
    path("<int:study_pk>/user/<int:user_pk>/accept/", views.accept, name="accept"),  # 신청 수락 (방장)
    path("<int:study_pk>/user/<int:user_pk>/deny/", views.deny, name="deny"),  # 신청 거절 (방장)
    path("<int:study_pk>/user/<int:user_pk>/kick/", views.kick, name="kick"),  # 스터디 추방 (방장)
    path("<int:study_pk>/withdraw/", views.withdraw, name="withdraw"),  # 스터디 탈퇴 (방장 제외)
    path("<int:notice_pk>/notice_delete/", views.notice_delete, name="notice_delete"),  # 알림 삭제
    path("notice_delete/all/", views.notice_delete_all, name="notice_delete_all"),  # 알림 전체 삭제
    path("notice_read/", views.notice_read, name="notice_read"),  # 알림 읽음
    path("<int:study_pk>/board/", views.board_index, name="board_index"),
    path("<int:study_pk>/board/index/1/", views.board_index_1, name="board_index_1"),
    path("<int:study_pk>/board/index/2/", views.board_index_2, name="board_index_2"),
    path("<int:study_pk>/board/index/3/", views.board_index_3, name="board_index_3"),
    path("<int:study_pk>/board/create/", views.board_create, name="board_create"),  # 스터디 게시판 글 작성
    path("<int:study_pk>/board/<int:article_pk>/", views.board_detail, name="board_detail"),  # 스터디 게시판 글 보기
    path("<int:study_pk>/board/<int:article_pk>/comment/", views.comment_create ,name="comment_create"),  # 스터디 게시판 댓글 작성
    path("<int:study_pk>/board/<int:article_pk>/comment/<int:comment_pk>/delete/", views.comment_delete, name="comment_delete"),  # 스터디 게시판 댓글 삭제
    path('search/',views.search, name='search' ),#검색
    # 검색 카테고리별
    path('search_al/', views.search_al, name='search_al'),
    path('search_fe/', views.search_fe, name='search_fe'),
    path('search_be/', views.search_be, name='search_be'),
    path('search_etc/', views.search_etc, name='search_etc'),
]
