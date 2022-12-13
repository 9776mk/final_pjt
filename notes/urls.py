from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.index, name="index"),
    path("sent/", views.sent, name="sent"),
    path("send/", views.send, name="send"),
    path("<int:pk>/reply/", views.reply, name="reply"),
    path("<int:user_pk>/send", views.send_to, name="send_to"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("trash/", views.trash, name="trash"),
    path("<int:pk>/trash_throw_away/", views.trash_throw_away, name="trash_throw_away"),
    path("<int:pk>/trash_return/", views.trash_return, name="trash_return"),
    path("important/", views.important, name="important"),
    path("<int:pk>/important_check/", views.important_check, name="important_check"),
    path("<int:pk>/important_return/", views.important_return, name="important_return"),
    path("trash/all_delete/", views.all_delete, name="all_delete"),# 휴지통 전체삭제
]