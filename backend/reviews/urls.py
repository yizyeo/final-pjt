from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.total_review_list, name='total_review_list'), 
    path('movies/<int:movie_pk>/', views.movie_review_list_or_create, name='movie_review_list_or_create'),
    path('<int:review_pk>/', views.review_detail_update_delete, name='review_detail_update_delete'),
    path('<int:review_pk>/like/', views.review_like, name='review_like'),

    path('<int:review_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:review_pk>/comments/<int:comment_pk>/', views.comment_delete, name='comment_delete'),

    path('blind/recommend/', views.get_blind_review_recommendations, name='blind_recommend'), # 리뷰 추천용 리뷰 가져오기
]