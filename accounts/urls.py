from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path(
        "is_valid_id/", views.is_valid_id, name="is_valid_id"
    ),  # 유효한 ID(username)인지 검사
    path("is_valid_bj_id/", views.is_valid_bj_id, name="is_valid_bj_id"),
    path("is_valid_git_id/", views.is_valid_git_id, name="is_valid_git_id"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<int:user_pk>/", views.profile, name="profile"),
    path("<int:user_pk>/update/", views.profile_update, name="profile_update"),
    path("password/", views.password, name="password"),  # 비밀번호 변경
    path("delete/", views.delete, name="delete"),  # 회원탈퇴
    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path("<int:user_pk>/guestbook/", views.guestbook, name="guestbook"),  # 방명록
    path(
        "<int:user_pk>/guestbook/article_create/",
        views.gb_article_create,
        name="gb_article_create",
    ),  # 방명록 글 작성
    path(
        "<int:user_pk>/guestbook/article/<int:gb_article_pk>/delete/",
        views.gb_article_delete,
        name="gb_article_delete",
    ),  # 방명록 글 삭제
    path(
        "<int:user_pk>/guestbook/article/<int:gb_article_pk>/comment_create/",
        views.gb_comment_create,
        name="gb_comment_create",
    ),  # 방명록 댓글 작성
    path(
        "<int:user_pk>/guestbook/article/<int:gb_article_pk>/comment/<int:gb_comment_pk>/delete/",
        views.gb_comment_delete,
        name="gb_comment_delete",
    ),  # 방명록 댓글 삭제
    path("login/github/", views.github_login, name="github-login"),  # 깃허브 로그인
    path(
        "login/github/callback/", views.github_login_callback, name="github-callback"
    ),  # 깃허브에서 callback 받아오는 URL
]
