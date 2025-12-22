from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # 모든 영화의 모든 리뷰
    path('', views.total_review_list, name='total_review_list'),
    # 특정 영화의 리뷰 목록 및 작성
    path('movies/<int:movie_pk>/', views.movie_review_list_or_create, name='movie_review_list_or_create'),
    # 리뷰 상세 조회, 수정, 삭제
    path('<int:review_pk>/', views.review_detail_update_delete, name='review_detail_update_delete'),
    # 좋아요
    path('<int:review_pk>/like/', views.review_like, name='review_like'),
    # 댓글 작성
    path('<int:review_pk>/comments/', views.comment_create, name='comment_create'),
    # 댓글 삭제
    path('<int:review_pk>/comments/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
]