from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('is_valid_id/', views.is_valid_id, name='is_valid_id'),    # 유효한 ID(username)인지 검사
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_pk>/', views.profile, name='profile'),
    path('<int:user_pk>/update/', views.profile_update, name='profile_update'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('<int:user_pk>/guestbook/', views.guestbook, name='guestbook'),    # 방명록
    path('<int:user_pk>/guestbook/article_create/', views.gb_article_create, name='gb_article_create'), # 방명록 글 작성
    path('<int:user_pk>/guestbook/article/<int:gb_article_pk>/delete/', views.gb_article_delete, name='gb_article_delete'), # 방명록 글 삭제
    path('<int:user_pk>/guestbook/article/<int:gb_article_pk>/comment_create/', views.gb_comment_create, name='gb_comment_create'), # 방명록 댓글 작성
]
