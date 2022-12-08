from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend/', views.recommend, name='recommend'),   # 랜덤 추천
]
