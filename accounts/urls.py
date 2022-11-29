from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path(
        "is_valid_id/", views.is_valid_id, name="is_valid_id"
    ),  # 유효한 ID(username)인지 검사
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<int:user_pk>/", views.profile, name="profile"),
    path("<int:user_pk>/update/", views.profile_update, name="profile_update"),
    path("login/github/", views.github_login, name="github-login"),
    path(
        "login/github/callback/",
        views.github_login_callback,
        name="github-callback",
    ),
]
