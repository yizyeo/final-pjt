from django.urls import path
from . import views

urlpatterns = [
    path('genres/', views.genre_list), # Gnere 테이블에 저장된 전체 장르 리스트를 반환
    path('backdrops/', views.carousel_backdrop),
    path('homelist/', views.home_list),

    path('movie/<int:movie_pk>/detail/', views.movie_detail),
    path('movie/<int:movie_pk>/like/', views.movie_like),
    path('movie/<int:movie_pk>/wish/', views.movie_wish),
    path('movie/<int:movie_pk>/watched/', views.movie_watched),
    path('movie/<int:movie_pk>/trailer/', views.movie_trailer),

    path('movielist/', views.movie_list),
    path('search/', views.search),
    path('worldcup/random/', views.random_worldcup),
    path('worldcup/user/', views.user_based_worldcup),

    path('recommend/keyword/', views.recommend_by_keyword),
]
