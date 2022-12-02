from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.index, name="index"),
    path("sent/", views.sent, name="sent"),
    path("send/", views.send, name="send"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]