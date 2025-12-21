from django.urls import path
from . import views

urlpatterns = [
    path('genres/', views.genre_list), # Gnere 테이블에 저장된 전체 장르 리스트를 반환
    path('backdrops/', views.carousel_backdrop),
    path('homelist/', views.home_list), # 
    path('movie/<int:movie_pk>/detail/', views.movie_detail),
    path('movielist/', views.movie_list),
]
