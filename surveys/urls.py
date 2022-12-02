from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    path('create/', views.create, name='create'),
]
