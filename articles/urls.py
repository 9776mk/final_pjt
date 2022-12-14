from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),#카테고리 
    path("index/1/", views.index_1, name="index_1"),#카테고리
    path("index/2/", views.index_2, name="index_2"),#카테고리
    path("index/3/", views.index_3, name="index_3"),#카테고리
    path("index/4/", views.index_4, name="index_4"),#카테고리
    path("friend", views.friend, name="friend"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path(
        "<int:article_pk>/comments_create/",
        views.comments_create,
        name="comments_create",
    ),
    path(
        "<int:article_pk>/comments_create/<int:comment_pk>/delete/",
        views.comments_delete,
        name="comments_delete",
    ),
    path("<int:article_pk>/likes/", views.likes, name="likes"),
    path('search/',views.search, name='search' ),#검색
    path('search/1/', views.search_1, name='search_1'),#검색
    path('search/2/', views.search_2, name='search_2'),#검색
    path('search/3/', views.search_3, name='search_3'),#검색
    path('search/4/', views.search_4, name='search_4'),#검색
    path(
        "<int:comment_pk>/profile_comments_delete/",
        views.profile_comments_delete,
        name="profile_comments_delete",
    ),
]
