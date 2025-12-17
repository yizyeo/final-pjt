from django.urls import path
from . import views

urlpatterns = [
    path('genres/', views.genre_list), # Gnere 테이블에 저장된 전체 장르 리스트를 반환
]
